from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, Document

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                  'phone_number', 'is_employer', 'is_seaman', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for user documents"""
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'user', 'is_verified', 'created_at', 'updated_at']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer with additional user info"""
    
    def validate(self, attrs):
        # Get the token
        data = super().validate(attrs)
        
        # Add custom claims
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_employer': user.is_employer,
            'is_seaman': user.is_seaman,
        }
        
        # Track login attempts (in a real implementation, this would be in a login view)
        user.last_login_attempt = None
        user.login_attempts = 0
        user.save(update_fields=['last_login_attempt', 'login_attempts'])
        
        return data

class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    is_employer = serializers.BooleanField(default=False)
    is_seaman = serializers.BooleanField(default=False)
    
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user is already registered with this email address.")
        return email
    
    def validate_password1(self, password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        if data['is_employer'] and data['is_seaman']:
            raise serializers.ValidationError("User cannot be both employer and seaman.")
        if not data['is_employer'] and not data['is_seaman']:
            raise serializers.ValidationError("User must be either employer or seaman.")
        return data
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_employer=validated_data.get('is_employer', False),
            is_seaman=validated_data.get('is_seaman', False),
        )
        user.set_password(validated_data['password1'])
        user.save()
        
        # Return the user instance
        return user

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset"""
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()
    
    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data