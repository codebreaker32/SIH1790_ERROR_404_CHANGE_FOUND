from twilio.rest import Client
from django.conf import settings

def send_sms_notification(self, report):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = (
        f"Match Found for Report ID: {report.report_id}. "
        f"Type: {report.report_type}, Location: {report.location}."
    )
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=self.phone_number
    )
