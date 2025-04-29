from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseTimestampModel(models.Model):
    """Abstract base model with created_at and updated_at fields"""
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True

class SavedSearch(models.Model):
    """Model for saved search queries by users"""
    from apps.accounts.models import User
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100)
    search_type = models.CharField(max_length=20, choices=[
        ('vacancy', 'Vacancy Search'),
        ('resume', 'Resume Search'),
    ])
    query_params = models.JSONField()
    auto_notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.search_type} by {self.user.email}"

class FavoriteItem(models.Model):
    """Model for users' favorite items (vacancies, resumes)"""
    from apps.accounts.models import User
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=20, choices=[
        ('vacancy', 'Vacancy'),
        ('resume', 'Resume'),
    ])
    object_id = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.content_type} favorite by {self.user.email}"

class SearchHistory(models.Model):
    """Model to track user search history"""
    from apps.accounts.models import User
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    search_type = models.CharField(max_length=20, choices=[
        ('vacancy', 'Vacancy Search'),
        ('resume', 'Resume Search'),
    ])
    query_params = models.JSONField()
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Search History")
        verbose_name_plural = _("Search History")
    
    def __str__(self):
        return f"{self.search_type} by {self.user.email} at {self.created_at}"

class ActivityLog(models.Model):
    """Model to track user activity"""
    from apps.accounts.models import User
    
    ACTION_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_vacancy', 'View Vacancy'),
        ('view_resume', 'View Resume'),
        ('create_vacancy', 'Create Vacancy'),
        ('create_resume', 'Create Resume'),
        ('update_vacancy', 'Update Vacancy'),
        ('update_resume', 'Update Resume'),
        ('apply', 'Apply to Vacancy'),
        ('message', 'Send Message'),
        ('search', 'Perform Search'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_type = models.CharField(max_length=50, blank=True)
    details = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} by {self.user.email} at {self.created_at}"