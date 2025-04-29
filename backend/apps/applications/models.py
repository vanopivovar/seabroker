from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.vacancies.models import Vacancy
from apps.resumes.models import Resume

class Application(models.Model):
    """Model representing a job application"""
    # Status choices
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('offer', 'Offer Extended'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    
    # Relationships
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    
    # Application details
    cover_letter = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_changed_at = models.DateTimeField(null=True, blank=True)
    
    # Notes (visible only to employer)
    employer_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        ordering = ['-created_at']
        # Prevent duplicate applications
        unique_together = ['applicant', 'vacancy']
    
    def __str__(self):
        return f"Application for {self.vacancy.title} by {self.applicant.email}"
        
class ApplicationStatusHistory(models.Model):
    """Model to track application status changes"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='status_changes')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Application Status History")
        verbose_name_plural = _("Application Status History")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application} status changed to {self.status}"