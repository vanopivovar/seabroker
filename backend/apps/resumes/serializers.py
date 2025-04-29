from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Resume, Experience, Education, Certificate
from apps.accounts.serializers import UserSerializer
from apps.vacancies.serializers import PositionSerializer, VesselTypeSerializer
from apps.vacancies.models import Position, VesselType

User = get_user_model()

class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for work experience"""
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['id', 'resume', 'created_at', 'updated_at']

class EducationSerializer(serializers.ModelSerializer):
    """Serializer for education entries"""
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['id', 'resume', 'created_at', 'updated_at']

class CertificateSerializer(serializers.ModelSerializer):
    """Serializer for certificates"""
    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ['id', 'resume', 'created_at', 'updated_at']

class ResumeListSerializer(serializers.ModelSerializer):
    """Serializer for resume list view"""
    seaman = UserSerializer(read_only=True)
    desired_position = PositionSerializer(read_only=True)
    preferred_vessel_types = VesselTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resume
        fields = [
            'id', 'seaman', 'title', 'desired_position',
            'preferred_vessel_types', 'total_experience_years',
            'desired_salary', 'desired_salary_currency',
            'availability', 'available_from',
            'is_active', 'is_featured', 'created_at',
            'views_count'
        ]
        read_only_fields = ['id', 'seaman', 'created_at', 'views_count']

class ResumeDetailSerializer(serializers.ModelSerializer):
    """Serializer for resume detail view"""
    seaman = UserSerializer(read_only=True)
    desired_position = PositionSerializer(read_only=True)
    preferred_vessel_types = VesselTypeSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    
    # For write operations
    desired_position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source='desired_position',
        write_only=True
    )
    preferred_vessel_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=VesselType.objects.all(),
        many=True,
        source='preferred_vessel_types',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['id', 'seaman', 'created_at', 'updated_at', 'views_count']
    
    def create(self, validated_data):
        # Extract and handle many-to-many relationships
        preferred_vessel_types = validated_data.pop('preferred_vessel_types', [])
        
        # Set the seaman to the current user
        validated_data['seaman'] = self.context['request'].user
        
        # Create the resume
        resume = Resume.objects.create(**validated_data)
        
        # Add the preferred vessel types
        if preferred_vessel_types:
            resume.preferred_vessel_types.set(preferred_vessel_types)
        
        return resume
    
    def update(self, instance, validated_data):
        # Extract and handle many-to-many relationships
        preferred_vessel_types = validated_data.pop('preferred_vessel_types', None)
        
        # Update the resume fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update the preferred vessel types if provided
        if preferred_vessel_types is not None:
            instance.preferred_vessel_types.set(preferred_vessel_types)
        
        return instance

class ResumeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating resumes"""
    desired_position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source='desired_position',
        write_only=True
    )
    preferred_vessel_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=VesselType.objects.all(),
        many=True,
        source='preferred_vessel_types',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Resume
        exclude = ['seaman', 'views_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract and handle many-to-many relationships
        preferred_vessel_types = validated_data.pop('preferred_vessel_types', [])
        
        # Set the seaman to the current user
        validated_data['seaman'] = self.context['request'].user
        
        # Create the resume
        resume = Resume.objects.create(**validated_data)
        
        # Add the preferred vessel types
        if preferred_vessel_types:
            resume.preferred_vessel_types.set(preferred_vessel_types)
        
        return resume