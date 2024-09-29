from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report, StaffUser

@receiver(post_save, sender=Report)
def send_notification_on_match(sender, instance, **kwargs):
    """
    Signal to notify the staff user when a match is found for a report.
    This assumes that the status field of the report is updated to 'Match Found'.
    """
    if instance.status == 'Match Found':
        # Get verified staff users who should receive the notification
        staff_users = StaffUser.objects.filter(is_verified=True)
        
        for staff in staff_users:
            staff.signal_found_person(instance)
