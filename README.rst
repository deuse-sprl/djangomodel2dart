++++++++++++++++
DjangoModel2Dart
++++++++++++++++

.. image:: https://img.shields.io/badge/version-0.1.0-blue
    :target: https://github.com/deuse-sprl/djangomodel2dart

.. image:: https://img.shields.io/github/license/deuse-sprl/djangomodel2dart
    :target: https://github.com/deuse-sprl/djangomodel2dart/blob/master/LICENSE

====================================================================
Python utility to transform Django Models to Dart serializer Classes
====================================================================

DjangoModel2Dart is a tool to help developers translate Django Model to Dart Serializer
classes. This is especially useful when working on a Flutter app with a Django Rest Framework
backend.


------------
Installation
------------
DjangoModel2Dart is a CLI utility developed in Python >=3.6.
To use the tool you have to pull it on your computer.

.. code-block::

    git pull git@github.com:deuse-sprl/djangomodel2dart.git

-----
Usage
-----
.. code-block::

    usage: djangomodel2dart.py [-h] [-c] name

    Python utility to transform Django Models to Dart serializer Classes

    positional arguments:
      name             Dart name of your model

    optional arguments:
      -h, --help       show this help message and exit
      -c, --camelcase  Transforms the names to CamelCase when snake_case (default: False)

To start using DjangoModel2Dart simply run :code:`python3 djangomodel2dart -c YourDesiredDartClassName` from
the folder where you pulled DjangoModel2Dart. This will open your preferred code editor
and if none is provided it will open VIM. Provide your ModelFields to translate in the editor.


-------
Example
-------
Example for a simple FAQ model.

.. code-block::

    class FrequentlyAskedQuestions(models.Model):
        question = models.CharField(verbose_name="Title of the question", max_length=255, blank=False, null=False)
        answer = models.CharField(verbose_name="Answer to the question", config_name='simple_toolbar', blank=True, null=True)
        expert = models.ForeignKey('Expert', verbose_name='Expert', on_delete=models.SET_NULL, null=True, blank=True)
        score = models.IntegerField(default=0, help_text="Score of the answer to the question")

Launch the script with following options:

.. code-block::

    python3 djangomodel2dart.py -c FrequentlyAskedQuestions

Your editor starts in which you provide the Model Fields, in this case :

.. code-block::

    question = models.CharField(verbose_name="Title of the question", max_length=255, blank=False, null=False)
    answer = models.CharField(verbose_name="Answer to the question", config_name='simple_toolbar', blank=True, null=True)
    expert = models.ForeignKey('Expert', verbose_name='Expert', on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default=0, help_text="Score of the answer to the question")

The CLI tool returns the following code structure and write it in a file named FrequentlyAskedQuestions.dart

.. code-block::

    class FrequentlyAskedQuestions
    {
        String? question;
        String? answer;
        'Expert'Model? expert;
        int? score;

        FrequentlyAskedQuestions {
            this.question,
            this.answer,
            this.expert,
            this.score,
        };

        FrequentlyAskedQuestions.fromJson(Map<String, dynamic> json):
            question = json[question],
            answer = json[answer],
            expert = json[expert],
            score = json[score];

        Map<String, dynamic> toJson() => {
            'question' : question,
            'answer' : answer,
            'expert' : expert,
            'score' : score,
        };
    }

**TADAAAA**

-----
About
-----
This tool is provided free of charge by `Deuse <https://www.deuse.be>`_ : a software engineering company
specialized in tailor-made developments and digital tools for bold projects.

------------
Contributing
------------
Thank you for considering contributing to DjangoModel2Dart. The main purpose of this repository is to continue evolving to make Flutter developer's lives easier.

Please report improvements, bugs and issues to Github's issue tracker.
Pull requests linked to open issues are even more appreciated.

We are also thrilled to receive a variety of other contributions including:

* Documentation updates, enhancements, designs, or bugfixes.
* Spelling or grammar fixes.
* Blogging, speaking about, or creating tutorials about DjangoModel2Dart.

**Giving us a Github star is much appreciated by our team ! Sharing our project with other Flutter developers is too :)**
