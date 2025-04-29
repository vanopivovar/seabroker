from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from allauth.account.signals import user_signed_up
from .models import User, Profile, Document
from apps.messages.models import EmailSubscription

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile for a new user"""
    if created:
        # Create user profile
        Profile.objects.create(user=instance)
        
        # Create email subscription preferences with default settings
        EmailSubscription.objects.create(user=instance)

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    """Handle user signup events"""
    # Additional processing for new user signups
    # For example, detecting user type based on registration source
    # or sending welcome emails
    pass