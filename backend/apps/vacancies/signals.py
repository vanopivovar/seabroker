from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Vacancy
from apps.core.models import ActivityLog
from apps.messages.models import Notification

@receiver(post_save, sender=Vacancy)
def vacancy_created_handler(sender, instance, created, **kwargs):
    """Handle vacancy creation events"""
    if created:
        # Log activity
        ActivityLog.objects.create(
            user=instance.employer,
            action='create_vacancy',
            object_id=instance.id,
            object_type='Vacancy',
            details={'title': instance.title}
        )
        
        # Create notifications for matching users
        # This would be implemented to notify users who have saved searches
        # that match this vacancy criteria
        pass

@receiver(pre_save, sender=Vacancy)
def vacancy_updated_handler(sender, instance, **kwargs):
    """Track changes to vacancies"""
    if instance.pk:
        try:
            old_instance = Vacancy.objects.get(pk=instance.pk)
            # Check if is_active status changed
            if old_instance.is_active != instance.is_active:
                # Additional handling for activation/deactivation
                pass
        except Vacancy.DoesNotExist:
            pass