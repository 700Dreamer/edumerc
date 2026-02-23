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
        message = f"A student ({instance.student.get_full_name() or instance.student.username}) has booked a session with you."
        details = [
            {'label': 'Booking ID', 'value': instance.booking_id},
            {'label': 'Date & Time', 'value': f"{instance.date} at {instance.start_time}"}
        ]
        html_body = gmail.get_html_template(
            title="New Booking Request!",
            message=message,
            details=details,
            button_text="View Appointments",
            button_url="https://edumerc.up.railway.app/coach/appointments", # Assuming this is the coach URL
            status="Pending"
        )
        gmail.send_email(instance.coach.user.email, subject, html_body, is_html=True)
    
    # Notify Student on status change
    else:
        # Check if status has changed (using simple check, could be improved by tracking old state)
        if instance.status == 'confirmed':
            subject = "Booking Confirmed - Complete your Payment"
            payment_init_url = f"https://edumerc.up.railway.app/pay-session/{instance.booking_id}"
            
            message = f"Your booking with {instance.coach.user.get_full_name() or instance.coach.user.username} has been confirmed."
            details = [
                {'label': 'Booking ID', 'value': instance.booking_id},
                {'label': 'Date & Time', 'value': f"{instance.date} at {instance.start_time}"},
                {'label': 'Total Price', 'value': f"{instance.total_price} UShs"}
            ]
            html_body = gmail.get_html_template(
                title="Booking Confirmed!",
                message=message,
                details=details,
                button_text="Pay Now",
                button_url=payment_init_url,
                status="Confirmed"
            )
            gmail.send_email(instance.student.email, subject, html_body, is_html=True)
            
        elif instance.status == 'cancelled':
            subject = "Booking Cancelled"
            message = f"Your booking with {instance.coach.user.get_full_name() or instance.coach.user.username} has been cancelled."
            details = [
                {'label': 'Booking ID', 'value': instance.booking_id},
                {'label': 'Date', 'value': str(instance.date)},
                {'label': 'Time', 'value': str(instance.start_time)}
            ]
            html_body = gmail.get_html_template(
                title="Booking Cancelled",
                message=message,
                details=details,
                status="Cancelled"
            )
            gmail.send_email(instance.student.email, subject, html_body, is_html=True)
