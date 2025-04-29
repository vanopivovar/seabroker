"""SeaJobs URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.core.views import health_check

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health check for Docker
    path('api/health/', health_check, name='health-check'),
    
    # API endpoints
    path('api/auth/', include('apps.accounts.urls.auth')),
    path('api/users/', include('apps.accounts.urls.users')),
    path('api/vacancies/', include('apps.vacancies.urls')),
    path('api/resumes/', include('apps.resumes.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/messages/', include('apps.messages.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)