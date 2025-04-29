from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification

@receiver(post_save, sender=Message)
def message_created_handler(sender, instance, created, **kwargs):
    """Handle new message creation events"""
    if created:
        # Get all participants except the sender
        recipients = instance.conversation.participants.exclude(id=instance.sender.id)
        
        # Create a notification for each recipient
        for recipient in recipients:
            Notification.objects.create(
                recipient=recipient,
                notification_type='message',
                title="New message",
                message=f"You received a new message from {instance.sender.get_full_name() or instance.sender.email}",
                related_object_id=instance.conversation.id,
                related_object_type='Conversation'
            )
            
            # If email notifications are enabled for this user and message type
            try:
                email_prefs = recipient.email_preferences
                if email_prefs.new_message:
                    # In a real app, we would send an email here
                    # For MVP, we just mark it as sent
                    pass
            except:
                # If email preferences don't exist, skip
                pass

@receiver(post_save, sender=Notification)
def notification_created_handler(sender, instance, created, **kwargs):
    """Handle notification creation events"""
    if created and not instance.is_email_sent:
        # Check if user wants email notifications for this type
        try:
            email_prefs = instance.recipient.email_preferences
            should_send_email = False
            
            # Check notification type against user preferences
            if instance.notification_type == 'message' and email_prefs.new_message:
                should_send_email = True
            elif instance.notification_type == 'application' and email_prefs.application_status_change:
                should_send_email = True
            elif instance.notification_type == 'vacancy' and email_prefs.new_matching_vacancy:
                should_send_email = True
            elif instance.notification_type == 'resume' and email_prefs.resume_viewed:
                should_send_email = True
            elif instance.notification_type == 'system' and email_prefs.account_updates:
                should_send_email = True
            
            if should_send_email:
                # In a real app, we would send an email here
                # For MVP, we just mark it as sent
                instance.is_email_sent = True
                instance.save(update_fields=['is_email_sent'])
                
        except:
            # If email preferences don't exist, skip
            pass