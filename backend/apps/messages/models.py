from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class Conversation(models.Model):
    """Model representing a conversation between users"""
    participants = models.ManyToManyField(User, related_name='conversations')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation {self.id} - {', '.join([user.email for user in self.participants.all()])}"

class Message(models.Model):
    """Model representing individual messages in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='message_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.email} in conversation {self.conversation.id}"

class Notification(models.Model):
    """Model representing system notifications"""
    # Notification types
    TYPE_CHOICES = (
        ('message', 'New Message'),
        ('application', 'Application Update'),
        ('vacancy', 'Vacancy Update'),
        ('resume', 'Resume View'),
        ('system', 'System Notification'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.email}"

class EmailSubscription(models.Model):
    """Model for managing email notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_preferences')
    
    # Message notifications
    new_message = models.BooleanField(default=True)
    
    # Application notifications
    application_status_change = models.BooleanField(default=True)
    new_application = models.BooleanField(default=True)
    
    # Vacancy notifications
    new_matching_vacancy = models.BooleanField(default=True)
    saved_search_results = models.BooleanField(default=True)
    
    # Resume notifications
    resume_viewed = models.BooleanField(default=True)
    
    # System notifications
    account_updates = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Email preferences for {self.user.email}"