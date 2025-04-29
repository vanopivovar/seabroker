from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User
from apps.vacancies.models import VesselType, Position

class Resume(models.Model):
    """Model representing a seaman's resume"""
    # Language proficiency choices
    LANGUAGE_PROFICIENCY = (
        ('basic', 'Basic'),
        ('conversational', 'Conversational'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    )
    
    # Availability choices
    AVAILABILITY_CHOICES = (
        ('immediate', 'Immediate'),
        ('1_week', '1 Week'),
        ('2_weeks', '2 Weeks'),
        ('1_month', '1 Month'),
        ('2_months', '2 Months'),
        ('3_months+', '3+ Months'),
    )
    
    # Basic information
    seaman = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    desired_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='resumes')
    preferred_vessel_types = models.ManyToManyField(VesselType, related_name='preferred_resumes')
    summary = models.TextField()
    
    # Experience details
    total_experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    
    # Desired job details
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_salary_currency = models.CharField(max_length=3, choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound')], default='USD')
    desired_contract_duration = models.PositiveIntegerField(help_text=_("Duration in months"), null=True, blank=True)
    
    # Availability
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='immediate')
    available_from = models.DateField(null=True, blank=True)
    
    # Skills and qualifications
    skills = models.TextField(blank=True)
    languages = models.TextField(blank=True, help_text=_("Format: Language (Proficiency Level), e.g., English (Fluent), Russian (Native)"))
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.desired_position} ({self.seaman.email})"

class Experience(models.Model):
    """Model representing work experience entries in a resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    vessel_name = models.CharField(max_length=255, blank=True)
    vessel_type = models.CharField(max_length=255, blank=True)
    vessel_dwt = models.CharField(max_length=50, blank=True, help_text=_("Deadweight tonnage"))
    flag = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company} ({self.start_date} - {self.end_date or 'Present'})"

class Education(models.Model):
    """Model representing education entries in a resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = _("Education")
        verbose_name_plural = _("Education")
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"

class Certificate(models.Model):
    """Model representing certificates in a resume"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"