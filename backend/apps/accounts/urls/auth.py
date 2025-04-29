from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from ..views import (
    CustomTokenObtainPairView,
    RegisterAPIView,
    PasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    # User registration
    path('register/', RegisterAPIView.as_view(), name='user-register'),
    
    # JWT authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Password reset
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]