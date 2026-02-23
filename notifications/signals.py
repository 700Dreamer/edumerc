from django.db.models.signals import post_save
from django.dispatch import receiver
from educoach.models import CoachingSession
from .services import GmailService

@receiver(post_save, sender=CoachingSession)
def session_notification_signal(sender, instance, created, **kwargs):
    gmail = GmailService()
    
    # Notify Coach on new booking
    if created:
        subject = "New Student Booking Request"
        body = (
            f"Hello {instance.coach.user.get_full_name() or instance.coach.user.username},\n\n"
            f"A student ({instance.student.get_full_name() or instance.student.username}) has booked a session with you.\n"
            f"Date: {instance.date}\n"
            f"Time: {instance.start_time}\n\n"
            f"Please log in to confirm the booking."
        )
        gmail.send_email(instance.coach.user.email, subject, body)
    
    # Notify Student on status change
    else:
        # Check if status has changed (using simple check, could be improved by tracking old state)
        if instance.status == 'confirmed':
            # Construct the payment link (frontend link that will hit the initiate-payment endpoint)
            payment_init_url = f"https://edumerc.up.railway.app/pay-session/{instance.booking_id}"
            
            subject = "Booking Confirmed - Complete your Payment"
            body = (
                f"Hello {instance.student.get_full_name() or instance.student.username},\n\n"
                f"Your booking with {instance.coach.user.get_full_name() or instance.coach.user.username} has been confirmed.\n"
                f"Date: {instance.date}\n"
                f"Time: {instance.start_time}\n"
                f"Meeting Link: {instance.meeting_link or 'N/A'}\n\n"
                f"IMPORTANT: Please complete your payment to secure this slot.\n"
                f"Click here to pay: {payment_init_url}\n\n"
                f"See you then!"
            )
            gmail.send_email(instance.student.email, subject, body)
            
        elif instance.status == 'cancelled':
            subject = "Booking Cancelled"
            body = (
                f"Hello {instance.student.get_full_name() or instance.student.username},\n\n"
                f"Your booking with {instance.coach.user.get_full_name() or instance.coach.user.username} on {instance.date} at {instance.start_time} has been cancelled.\n"
            )
            gmail.send_email(instance.student.email, subject, body)
