
class Pump
{
    String? email;
    String? firstName;
    String? lastName;
    String? street;
    String? zipCode;
    String? city;
    String? country;
    String? language;
    String? status;
    String? type;
    String? phoneNumber;
    String? serialNumber;
    DateTime? dateBuy;
    bool? completedSignUp;


    Pump ({
        this.email,
        this.firstName,
        this.lastName,
        this.street,
        this.zipCode,
        this.city,
        this.country,
        this.language,
        this.status,
        this.type,
        this.phoneNumber,
        this.serialNumber,
        this.dateBuy,
        this.completedSignUp,
    });

    Pump.fromJson(Map<String, dynamic> json):
        email = json['email'], 
        firstName = json['first_name'], 
        lastName = json['last_name'], 
        street = json['street'], 
        zipCode = json['zip_code'], 
        city = json['city'], 
        country = json['country'], 
        language = json['language'], 
        status = json['status'], 
        type = json['type'], 
        phoneNumber = json['phone_number'], 
        serialNumber = json['serial_number'], 
        dateBuy = json['date_buy'], 
        completedSignUp = json['completed_sign_up'];

    Map<String, dynamic> toJson() => {
        'email' : email, 
        'first_name' : firstName, 
        'last_name' : lastName, 
        'street' : street, 
        'zip_code' : zipCode, 
        'city' : city, 
        'country' : country, 
        'language' : language, 
        'status' : status, 
        'type' : type, 
        'phone_number' : phoneNumber, 
        'serial_number' : serialNumber, 
        'date_buy' : dateBuy.toString(), 
        'completed_sign_up' : completedSignUp.toString(),
    };
}
