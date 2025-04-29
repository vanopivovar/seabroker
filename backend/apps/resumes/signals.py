from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Resume
from apps.core.models import ActivityLog
from apps.messages.models import Notification

@receiver(post_save, sender=Resume)
def resume_created_handler(sender, instance, created, **kwargs):
    """Handle resume creation events"""
    if created:
        # Log activity
        ActivityLog.objects.create(
            user=instance.seaman,
            action='create_resume',
            object_id=instance.id,
            object_type='Resume',
            details={'title': instance.title}
        )

@receiver(pre_save, sender=Resume)
def resume_updated_handler(sender, instance, **kwargs):
    """Track changes to resumes"""
    if instance.pk:
        try:
            old_instance = Resume.objects.get(pk=instance.pk)
            # Check if is_active status changed
            if old_instance.is_active != instance.is_active:
                # Additional handling for activation/deactivation
                pass
                
            # Track view count separately to prevent overwriting
            if old_instance.views_count != instance.views_count:
                # If someone viewed the resume, notify the owner
                # but only if this is an actual view (not an edit)
                if instance.views_count > old_instance.views_count:
                    Notification.objects.create(
                        recipient=instance.seaman,
                        notification_type='resume',
                        title="Your resume was viewed",
                        message=f"Your resume '{instance.title}' was viewed by an employer",
                        related_object_id=instance.id,
                        related_object_type='Resume'
                    )
        except Resume.DoesNotExist:
            pass