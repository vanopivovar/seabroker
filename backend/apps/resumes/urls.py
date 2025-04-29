from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ResumeViewSet, ExperienceViewSet, EducationViewSet, CertificateViewSet

# Create a router for resumes
router = DefaultRouter()
router.register(r'', ResumeViewSet, basename='resume')

# Create nested routers for resume-related resources
resume_router = routers.NestedSimpleRouter(router, r'', lookup='resume')
resume_router.register(r'experiences', ExperienceViewSet, basename='resume-experience')
resume_router.register(r'educations', EducationViewSet, basename='resume-education')
resume_router.register(r'certificates', CertificateViewSet, basename='resume-certificate')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Include the nested router URLs
    path('', include(resume_router.urls)),
]