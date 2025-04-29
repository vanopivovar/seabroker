from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile, Document
from .serializers import (
    UserSerializer, ProfileSerializer, DocumentSerializer,
    CustomTokenObtainPairSerializer, RegisterSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view with additional user info"""
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # Check if the user has too many failed login attempts
        email = request.data.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                max_attempts = getattr(settings, 'MAX_LOGIN_ATTEMPTS', 5)
                timeout = getattr(settings, 'LOGIN_ATTEMPT_TIMEOUT', 300)  # 5 minutes
                
                # Check if user is locked out
                if user.login_attempts >= max_attempts and user.last_login_attempt:
                    # Check if the lockout period has passed
                    lockout_time = user.last_login_attempt
                    time_diff = (timezone.now() - lockout_time).total_seconds()
                    
                    if time_diff < timeout:
                        return Response(
                            {"detail": f"Too many failed login attempts. Please try again in {int((timeout - time_diff) / 60)} minutes."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS
                        )
                
                # Track login attempt
                user.last_login_attempt = timezone.now()
                user.login_attempts += 1
                user.save(update_fields=['last_login_attempt', 'login_attempts'])
                
            except User.DoesNotExist:
                # Do nothing, let normal authentication flow handle it
                pass
        
        return super().post(request, *args, **kwargs)

class RegisterAPIView(generics.CreateAPIView):
    """API view for user registration"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate verification email (in a real app)
        # For MVP we skip email verification
        
        # Return the created user
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile
        return Profile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Update current user's profile"""
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for user documents"""
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own documents
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Set the user automatically
        serializer.save(user=self.request.user)

class PasswordResetView(APIView):
    """API view for requesting a password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # In a real app, send an email with the reset link
            # For MVP, we just return the token and uid
            # SECURITY NOTE: In production, do NOT return these directly to the frontend
            reset_url = f"/reset-password/{uid}/{token}/"
            
            return Response({
                "detail": "Password reset email has been sent.",
                "dev_info": {
                    "uid": uid,
                    "token": token,
                    "reset_url": reset_url
                }
            })
            
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            return Response({
                "detail": "Password reset email has been sent."
            })

class PasswordResetConfirmView(APIView):
    """API view for confirming a password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
            
            # Check the token
            if default_token_generator.check_token(user, serializer.validated_data['token']):
                # Set the new password
                user.set_password(serializer.validated_data['new_password1'])
                user.save()
                
                return Response({
                    "detail": "Password has been reset successfully."
                })
            else:
                return Response({
                    "detail": "Invalid reset token."
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                "detail": "Invalid user ID."
            }, status=status.HTTP_400_BAD_REQUEST)