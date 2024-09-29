from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import uuid

class public_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)  # Ensure unique phone numbers
    otp = models.CharField(max_length=6, blank=True)
    verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(null=True, blank=True)  # Track OTP creation time
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now= True, null=True, blank=True)

    def __str__(self):
        return self.phone_number

    def otp_is_valid(self):
        """
        Check if the OTP is still valid based on the creation time.
        This assumes an OTP expiration of 5 minutes.
        """
        if not self.otp_created_at:
            return False
        return timezone.now() <= self.otp_created_at + timedelta(minutes=5)


class ReportMatch(models.Model):
    report = models.OneToOneField('Report', on_delete=models.CASCADE, related_name="match")
    location = models.CharField(max_length=255, null = True, blank=True)  # Location where the person/item was detected
    timestamp = models.DateTimeField(default=timezone.now)  # Time when the match was detected
    additional_data = models.JSONField(default=dict, null = True, blank=True)  # Store additional data as a JSON field

    def __str__(self):
        return f"Match for {self.report.report_id} at {self.location} on {self.timestamp}"

    def append_match_data(self, new_data, location=None):
        """
        Appends new data to the existing match instance.
        Updates the location and timestamp as needed.
        """
        # Update the location and timestamp if new data is provided
        if location:
            self.location = location
        self.timestamp = timezone.now()

        # Append the new data into the JSON field
        if isinstance(self.additional_data, dict):
            self.additional_data.update(new_data)
        else:
            raise ValueError("Additional data must be a dictionary.")
        self.save()

class Report(models.Model):
    REPORT_TYPES = [
        ('Missing Person', 'Missing Person'),
        ('Lost Item', 'Lost Item'),
    ]
    gender_choices = [
        ('Male', 'male'),
        ('Female', 'female'),
        ('Other', 'other'),
    ]

    Status_types = [
        ('Pending', 'Pending'),
        ('Found', 'Found'),
        ('Closed', 'Closed'),
    ]
    user = models.ForeignKey(public_user, on_delete=models.CASCADE, related_name="reports")
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    description = models.TextField()
    last_seen_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=Status_types, default='Pending') # read only
    timestamp = models.DateTimeField(auto_now_add=True)
    report_id = models.CharField(max_length=10, unique=True, blank=True)  # Allow auto-generation

    def __str__(self):
        return f"{self.report_type} report by {self.user.phone_number} at {self.timestamp}"

    def save(self, *args, **kwargs):
        # Generate a new report_id at the time of creation using UUID
        if not self.report_id:
            self.report_id = self.generate_unique_report_id()
        super().save(*args, **kwargs)

    def generate_unique_report_id(self):
        # Generate a unique ID using UUID and return the first 8 characters
        return "RP" + str(uuid.uuid4()).split('-')[0].upper()  # Example format: RP4E5F6A8C
    
    def add_or_update_match(self, location, match_data):
        """
        Either create a new match or update the existing match with new data.
        """
        if hasattr(self, 'match'):
            # If a match already exists, append the new data
            self.match.append_match_data(new_data=match_data, location=location)
        else:
            # Create a new match if it doesn't exist
            ReportMatch.objects.create(
                report=self,
                location=location,
                additional_data=match_data
            )
            # Update report status to "Match Found"
            self.status = "Match Found"
            self.save()


class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    notification_preference = models.CharField(max_length=50, choices=[('SMS', 'SMS')], default='SMS')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Staff"

    def signal_found_person(self, report):
        """
        Send a notification (SMS) to the user when a match is found.
        """
        if self.notification_preference == 'SMS':
            self.send_sms_notification(report)

    def send_sms_notification(self, report):
        """
        Sends an SMS notification to the user about the found person/item.
        You need to integrate this with an actual SMS service like Twilio.
        """
        message = (
            f"Match Found for Report ID: {report.report_id}. "
            f"Type: {report.report_type}, Location: {report.location}."
        )
        print(f"Sending SMS to {self.phone_number}: {message}")
        # Integrate with an SMS API like Twilio to send the SMS

