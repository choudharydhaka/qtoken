import twilio
import twilio.rest

try:
    client = twilio.rest.TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(
        body="Hello World",
        to="+14159352345",
        from_="+14158141829"
    )
except twilio.TwilioRestException as e:
    print(e)
