from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = "AC3e9a17f13b37d3a4cdee98f6e3b7f894"
AUTH_TOKEN = "8ace0f9ae269dfe81dfb9785c62c907e"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

sms = client.sms.messages.create(body="haha, gofree, yo",
    to="+8613828414757",
    from_="+12057694613",
)

print sms.body
