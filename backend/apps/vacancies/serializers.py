from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VesselType, Position, Vacancy
from apps.accounts.serializers import UserSerializer

User = get_user_model()

class VesselTypeSerializer(serializers.ModelSerializer):
    """Serializer for vessel types"""
    class Meta:
        model = VesselType
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    """Serializer for job positions"""
    class Meta:
        model = Position
        fields = '__all__'

class VacancyListSerializer(serializers.ModelSerializer):
    """Serializer for vacancy list view"""
    employer = UserSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    vessel_type = VesselTypeSerializer(read_only=True)
    
    class Meta:
        model = Vacancy
        fields = [
            'id', 'title', 'employer', 'position', 'vessel_type',
            'location', 'contract_type', 'experience_level',
            'salary_min', 'salary_max', 'salary_currency',
            'is_active', 'is_featured', 'application_deadline',
            'created_at', 'views_count'
        ]
        read_only_fields = ['id', 'employer', 'created_at', 'views_count']

class VacancyDetailSerializer(serializers.ModelSerializer):
    """Serializer for vacancy detail view"""
    employer = UserSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    vessel_type = VesselTypeSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source='position',
        write_only=True
    )
    vessel_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VesselType.objects.all(),
        source='vessel_type',
        write_only=True
    )
    
    class Meta:
        model = Vacancy
        fields = '__all__'
        read_only_fields = ['id', 'employer', 'created_at', 'updated_at', 'views_count']
    
    def create(self, validated_data):
        # Set the employer to the current user
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)

class VacancyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating vacancies"""
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source='position',
        write_only=True
    )
    vessel_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VesselType.objects.all(),
        source='vessel_type',
        write_only=True
    )
    
    class Meta:
        model = Vacancy
        exclude = ['employer', 'views_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the employer to the current user
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)