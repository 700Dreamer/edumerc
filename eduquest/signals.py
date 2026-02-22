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
            body = (
                f"Hello {user_name},\n\n"
                f"Great news! Your EduQuest material order ({instance.reference}) for {instance.school_name} has been APPROVED.\n"
                f"Total Sets: {instance.total_sets}\n"
                f"Estimated Amount: UGX {instance.estimated_amount}\n"
            )
            
            if instance.expected_delivery_date:
                body += f"Expected Delivery Date: {instance.expected_delivery_date}\n\n"
            else:
                body += "\n"

            body += (
                f"Please log in to your dashboard to complete the payment for this order.\n\n"
                f"Thank you,\nThe Edumerk Team"
            )
            gmail.send_email(user_email, subject, body)
            
        elif instance.status == 'DECLINED':
            subject = f"EduQuest Order Declined: {instance.reference}"
            body = (
                f"Hello {user_name},\n\n"
                f"We regret to inform you that your EduQuest material order ({instance.reference}) for {instance.school_name} has been DECLINED.\n\n"
                f"If you have any questions, please contact our support team.\n\n"
                f"Thank you,\nThe Edumerk Team"
            )
            gmail.send_email(user_email, subject, body)

        elif instance.status == 'PAID':
            subject = f"Payment Received: {instance.reference}"
            body = (
                f"Hello {user_name},\n\n"
                f"We have successfully received your payment for EduQuest material order ({instance.reference}).\n\n"
                f"We will begin processing your order for {instance.school_name} immediately.\n\n"
                f"Thank you,\nThe Edumerk Team"
            )
            gmail.send_email(user_email, subject, body)
