from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User

class VesselType(models.Model):
    """Model representing types of vessels"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Position(models.Model):
    """Model representing job positions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class Vacancy(models.Model):
    """Model representing job vacancies"""
    # Contract type choices
    CONTRACT_CHOICES = (
        ('permanent', 'Permanent'),
        ('fixed_term', 'Fixed-term'),
        ('temporary', 'Temporary'),
        ('rotational', 'Rotational'),
    )
    
    # Salary currency choices
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    )
    
    # Experience level choices
    EXPERIENCE_CHOICES = (
        ('entry', 'Entry Level'),
        ('junior', 'Junior'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior'),
        ('expert', 'Expert'),
    )
    
    # Basic information
    title = models.CharField(max_length=255)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacancies')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='vacancies')
    vessel_type = models.ForeignKey(VesselType, on_delete=models.PROTECT, related_name='vacancies')
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    
    # Location and details
    location = models.CharField(max_length=255, blank=True)
    vessel_name = models.CharField(max_length=255, blank=True)
    vessel_flag = models.CharField(max_length=100, blank=True)
    
    # Contract details
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES)
    contract_duration = models.PositiveIntegerField(help_text=_("Duration in months"), null=True, blank=True)
    rotation_duration = models.CharField(max_length=50, blank=True, help_text=_("e.g., '2 months on, 2 months off'"))
    
    # Compensation
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    
    # Requirements
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    required_certificates = models.TextField(blank=True)
    required_languages = models.TextField(blank=True)
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancies")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.vessel_type} ({self.employer.email})"