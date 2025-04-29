from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Application, ApplicationStatusHistory
from apps.core.models import ActivityLog
from apps.messages.models import Notification

@receiver(post_save, sender=Application)
def application_created_handler(sender, instance, created, **kwargs):
    """Handle application creation events"""
    if created:
        # Log activity for the applicant
        ActivityLog.objects.create(
            user=instance.applicant,
            action='apply',
            object_id=instance.vacancy.id,
            object_type='Vacancy',
            details={'title': instance.vacancy.title}
        )
        
        # Create initial status history
        ApplicationStatusHistory.objects.create(
            application=instance,
            status=instance.status,
            changed_by=instance.applicant,
            notes="Initial application submitted"
        )
        
        # Notify the employer
        Notification.objects.create(
            recipient=instance.vacancy.employer,
            notification_type='application',
            title="New job application",
            message=f"You received a new application for '{instance.vacancy.title}'",
            related_object_id=instance.id,
            related_object_type='Application'
        )

@receiver(pre_save, sender=Application)
def application_status_change_handler(sender, instance, **kwargs):
    """Track application status changes"""
    if instance.pk:
        try:
            old_instance = Application.objects.get(pk=instance.pk)
            # Check if status has changed
            if old_instance.status != instance.status:
                # Update status change timestamp
                instance.status_changed_at = timezone.now()
                
                # Create status history entry (will be updated with changed_by in view)
                ApplicationStatusHistory.objects.create(
                    application=instance,
                    status=instance.status,
                    notes=f"Status changed from {old_instance.status} to {instance.status}"
                )
                
                # Notify the applicant
                Notification.objects.create(
                    recipient=instance.applicant,
                    notification_type='application',
                    title="Application status updated",
                    message=f"Your application for '{instance.vacancy.title}' has been updated to: {instance.get_status_display()}",
                    related_object_id=instance.id,
                    related_object_type='Application'
                )
        except Application.DoesNotExist:
            pass