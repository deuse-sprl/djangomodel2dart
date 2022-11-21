import re, tempfile, os
import argparse
from subprocess import call

EDITOR = os.environ.get('EDITOR', 'vim')

initial_message = b"""
    # YOUR INPUT STRING IN THE FORMAT: VARIABLE_NAME = models.VARIABLE_TYPE(attributes). Maximum 1 line per field. e.g.:
    # question = models.CharField(verbose_name="Title of the question", max_length=255, blank=False, null=False)
    # answer = models.CharField(verbose_name="Answer to the question", config_name='simple_toolbar', blank=True, null=True)
    # expert = models.ForeignKey('Expert', verbose_name='Expert', on_delete=models.SET_NULL, null=True, blank=True)
    # score = models.IntegerField(default=0, help_text="Score of the answer to the question")
"""


def transform(input_string, dart_model_name, reformat_case_variable):
    """ Method to transform the fields of a Django Model into a Dart serializer class.

    It currently supports the following Django Model Field types :
        - CharField
        - TextField
        - BooleanField
        - IntegerField
        - FloatField (String)
        - TimeField
        - DateField
        - ForeignKey (replace the first attribute by itself
            + Model, eg: User -> UserModel)
        - MultiSelectField (considered as String)
        - LowercaseEmailField (String)

    :param input_string: The multiline string containing the django model fields
    :param dart_model_name: The name of the desired Dart class
    :param reformat_case_variable: Boolean, if true transforms the snake_case into a CamelCase
    :return:
    """
    dart_string = ""
    dart_constructor_string = ""
    dart_from_json_string = ""
    dart_to_json_string = ""
    for line in input_string.splitlines():
        if line == "" or line.strip().startswith("#"):
            continue

        # Get variable name
        list_values = line.split("=")
        var_name = ""
        var_name_snake = list_values[0].strip()
        if reformat_case_variable:
            var_name = to_camel_case(list_values[0]).strip()
        else:
            var_name = var_name_snake

        # Get variable type
        gross_type = list_values[1].strip()
        python_type = ""
        python_ref = ""
        dart_type = ""
        dart_ref = ""

        # Look for django base models
        base_model = re.search("^models.(.*)\(.*$", gross_type)
        # Look for custom models
        custom_model = re.search("^(.*)\(.*$", gross_type)

        if base_model:
            python_type = base_model.group(1).strip()
        elif custom_model:
            python_type = custom_model.group(1).strip()

        # If we have a foreignKey we have to look for referenced model
        if python_type == "ForeignKey":
            referenced_model = re.search("^.*\((.*),.*$", gross_type)
            python_ref = referenced_model.group(1)
            dart_ref = python_ref + "Model"

        # We make the match between Django models and Dart types
        if python_type == "CharField":
            dart_type = "String"
        if python_type == "TextField":
            dart_type = "String"
        elif python_type == "BooleanField":
            dart_type = "bool"
        elif python_type == "IntegerField":
            dart_type = "int"
        elif python_type == "FloatField":
            dart_type = "double"
        elif python_type == "TimeField":
            dart_type = "String"
        elif python_type == "DateField":
            dart_type = "DateTime"
        elif python_type == "ForeignKey":
            dart_type = dart_ref
        elif python_type == "MultiSelectField":
            dart_type = "String"
        elif python_type == "LowercaseEmailField":
            dart_type = "String"

        dart_model = f"{4*' '}{dart_type}? {var_name};"

        # List of variables
        dart_string += f"{dart_model}\n"

        # Constructor
        dart_constructor_string += f"{8*' '}this.{var_name},\n"

        # From json
        dart_from_json_string += f"{8*' '}{var_name} = json[{var_name_snake}], \n"

        # To json
        dart_to_json_string += f"{8*' '}'{var_name_snake}' : {var_name}, \n"

    # Replace last character of string with ';'
    dart_from_json_string = dart_from_json_string.strip()[:-1] + ";"

    return f"""
class {dart_model_name}

{{
{dart_string}

{4*' '}{dart_model_name} {{
{dart_constructor_string}
{4*' '}}};

{4*' '}{dart_model_name}.fromJson(Map<String, dynamic> json):
{8*' '}{dart_from_json_string}

{4*' '}Map<String, dynamic> toJson() => {{
{dart_to_json_string}
{4*' '}}};
}}
"""


def to_camel_case(snake_str):
    """ Transforms a snake_case string (PEP8) into a camelCase string (Dart). """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


# Argument Parser for the arguments of our python script.
parser = argparse.ArgumentParser(description="Python utility to transform Django Models to Dart serializer Classes",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--camelcase", action="store_true", help="Transforms the names to CamelCase when snake_case")
parser.add_argument("name", help="Dart name of your model")
args = parser.parse_args()
config = vars(args)

# Parameter to says if we should reformat variable from snake_case to camelCase
reformat_case_variable = config.get("camelcase")

# Name of the model in Dart
dart_model_name = config.get("name")


# creates a temporary file with an example to open up in VIM for editing. Then returns the Dart Serializer
# of the provided content (Django Model Field list).
with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    tf.write(initial_message)
    tf.flush()
    call([EDITOR, "+set backupcopy=yes", tf.name])

    tf.seek(0)
    edited_message = tf.read().decode("utf-8")

    dart_serializers = transform(edited_message, dart_model_name, reformat_case_variable)

    # print the output in the console
    print(dart_serializers)

