from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Application, ApplicationStatusHistory
from apps.accounts.serializers import UserSerializer
from apps.vacancies.serializers import VacancyListSerializer
from apps.resumes.serializers import ResumeListSerializer
from apps.vacancies.models import Vacancy
from apps.resumes.models import Resume

User = get_user_model()

class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for application status history"""
    changed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ApplicationStatusHistory
        fields = '__all__'
        read_only_fields = ['id', 'application', 'created_at']

class ApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for application list view"""
    applicant = UserSerializer(read_only=True)
    vacancy = VacancyListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'applicant', 'vacancy', 'status',
            'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applicant', 'created_at', 'updated_at']

class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Serializer for application detail view"""
    applicant = UserSerializer(read_only=True)
    vacancy = VacancyListSerializer(read_only=True)
    resume = ResumeListSerializer(read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = [
            'id', 'applicant', 'created_at', 'updated_at',
            'status_changed_at', 'status_history', 'employer_notes'
        ]

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""
    vacancy_id = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.filter(is_active=True),
        source='vacancy',
        write_only=True
    )
    resume_id = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.filter(is_active=True),
        source='resume',
        write_only=True
    )
    
    class Meta:
        model = Application
        fields = [
            'vacancy_id', 'resume_id', 'cover_letter',
            'expected_salary', 'availability_date'
        ]
    
    def validate(self, data):
        """
        Validate the application data
        """
        user = self.context['request'].user
        
        # Check if user is a seaman
        if not user.is_seaman:
            raise serializers.ValidationError("Only seamen can apply for vacancies")
        
        # Check if the resume belongs to the applicant
        if data['resume'].seaman != user:
            raise serializers.ValidationError("You can only apply with your own resume")
        
        # Check if user has already applied to this vacancy
        vacancy = data['vacancy']
        if Application.objects.filter(applicant=user, vacancy=vacancy).exists():
            raise serializers.ValidationError("You have already applied to this vacancy")
        
        return data
    
    def create(self, validated_data):
        # Set the applicant to the current user
        validated_data['applicant'] = self.context['request'].user
        
        # Create the application
        return super().create(validated_data)

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application status"""
    notes = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = Application
        fields = ['status', 'notes']
    
    def validate(self, data):
        """
        Validate the status update
        """
        user = self.context['request'].user
        application = self.instance
        
        # Check if user is authorized to update status
        if application.vacancy.employer != user and not user.is_staff:
            raise serializers.ValidationError("Only the employer or staff can update application status")
        
        # Validate status transition
        current_status = application.status
        new_status = data['status']
        
        # Add any specific status transition rules here if needed
        # For example, preventing going back from 'rejected' to 'pending'
        
        return data
    
    def update(self, instance, validated_data):
        """
        Update the application status and create a status history entry
        """
        notes = validated_data.pop('notes', '')
        user = self.context['request'].user
        
        # Update the application
        instance = super().update(instance, validated_data)
        
        # Create status history entry
        ApplicationStatusHistory.objects.create(
            application=instance,
            status=instance.status,
            changed_by=user,
            notes=notes
        )
        
        return instance