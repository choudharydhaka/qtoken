# **qtoken**
This is qtoken store application to help any govt/stores to allow people to give order online and help them to avoid any un for State Govt of India

# Audiance
- Developers
- Anyone who want to utilize this functionality







## Twilio settings for the APP
Please setup below mentioned values with your Twilio account creadentials and, copy and paste it to file [settings](qtoken\settings.py)
```
TWILIO_ACCOUNT_SID = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Your Auth Token from twilio.com/console
TWILIO_AUTH_TOKEN  = "your_auth_token"

# Your Message service ID https://www.twilio.com/console/sms/services
TWILIO_MESSAGING_SERVICE_SID="MESGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#TWILIO_FROM_MOBILE='+512488566'
TWILIO_FROM_MOBILE='+YOUR_TWILIO_PURCHASED_NUMBER'
#TWILIO_TO_COUNTRY_CODE='+91'
TWILIO_TO_COUNTRY_CODE='+COUNTRY_CODE_TO_SEND_SMS'
```

## Getting started

## Prerequisite
- Python 3.8 (https://www.python.org/downloads/)
- Pip (Bundled with Python)
- Django (https://www.djangoproject.com/)
    - Install ```pip install Django==3.0.6 ```
    - How to install official docs (https://www.djangoproject.com/download/)
- Twilio Pythong package
    - ```pip install twilio```
## How to install QToken app
- Clone the project ```git clone git@github.com:choudharydhaka/qtoken.git```
- Please run the below commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8080
```
# **How to access?**
## **Store Registrations and orders for Store Owners**
You will have to register the stores below any consumer make any request for Liquor

- Step 1: goto your browser and type:
 ``` http://127.0.0.1:8080/stores/```, this page will ask you to register both store details and owner details

  ![](/.attachments/s-submit-1.png)

 Once you submitted the details, it will generate a STORE ID for you, 
 > STORE ID is a unique value, you will not be able to get it again, so please note it down safely

   ![](/.attachments/s-submit-success.PNG)

> You cant register same Store two times
![](/.attachments/s-submit-error.PNG)

 - Step 2: Now Consumer can place the order for you, and you will be able to get the tokens for your store at below mentioned addresses
    - Get all the orders for current Hours (it's 1 hour limit) - 
``` http://127.0.0.1:8080/liquor/stores/<STORE_ID>```
![](/.attachments/t-now.PNG)
    - Get all the orders for today - 
    ``` http://127.0.0.1:8080/liquor/stores/<STORE_ID>/today```
    ![](/.attachments/t-today.PNG)
    - Get all the orders for your Liquor store - 
    ``` http://127.0.0.1:8080/liquor/stores/<STORE_ID>/all```
![](/.attachments/t-all.PNG)


## **Consumer order placement**
You will have to provide a bunch of details in order to place a order. 
#### Search Store
Please provide area pincode to search any registered store
- Search Store registered on given area pincode - 
``` http://127.0.0.1:8080/liquor/ ```

![](/.attachments/search-store.PNG)

> If there is not store is registered you will not get any other details.

![](/.attachments/search-store-nf.PNG)

- Now click on "Get Store" button to get the available slots and the Stores registered


#### Place order
- Once you find a store, now you can place your order by providing your details and click on "Get Token" button.
  ![](/.attachments/c-order.PNG)

- Once your order will be placed you will get a SMS with your token number. Please bring the token number to Store to get your items.
  ![](/.attachments/c-confirmed-success.PNG)

- If you will provide a wrong mobile number or any issue there to send the SMS with the system you will still get your token number.
  ![](/.attachments/c-confirmed.PNG)


# Thanks
