from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaterialOrder
from notifications.services import GmailService

@receiver(post_save, sender=MaterialOrder)
def material_order_notification_signal(sender, instance, created, **kwargs):
    gmail = GmailService()
    
    # We only notify when the status changes after creation
    if not created:
        user_email = instance.email or instance.user.email # Fallback to user email if order email is blank
        if not user_email:
            return  # Can't notify without an email

        user_name = instance.user.get_full_name() or instance.user.username

        if instance.status == 'APPROVED':
            subject = f"EduQuest Order Approved: {instance.reference}"
            message = f"Great news! Your EduQuest material order for {instance.school_name} has been APPROVED."
            details = [
                {'label': 'Order Ref', 'value': instance.reference},
                {'label': 'Total Sets', 'value': str(instance.total_sets)},
                {'label': 'Amount', 'value': f"UGX {instance.estimated_amount}"}
            ]
            if instance.expected_delivery_date:
                details.append({'label': 'Expected Delivery', 'value': str(instance.expected_delivery_date)})
            
            html_body = gmail.get_html_template(
                title="Order Approved!",
                message=message,
                details=details,
                button_text="Go to Dashboard",
                button_url="https://edumerc.up.railway.app/dashboard",
                status="Approved"
            )
            gmail.send_email(user_email, subject, html_body, is_html=True)
            
        elif instance.status == 'DECLINED':
            subject = f"EduQuest Order Declined: {instance.reference}"
            message = f"We regret to inform you that your EduQuest material order for {instance.school_name} has been DECLINED."
            details = [{'label': 'Order Ref', 'value': instance.reference}]
            html_body = gmail.get_html_template(
                title="Order Declined",
                message=message,
                details=details,
                status="Declined"
            )
            gmail.send_email(user_email, subject, html_body, is_html=True)

        elif instance.status == 'PAID':
            subject = f"Payment Received: {instance.reference}"
            message = f"We have successfully received your payment for order {instance.reference}. We will begin processing it for {instance.school_name} immediately."
            details = [{'label': 'Order Ref', 'value': instance.reference}]
            html_body = gmail.get_html_template(
                title="Payment Received!",
                message=message,
                details=details,
                status="Paid"
            )
            gmail.send_email(user_email, subject, html_body, is_html=True)
