from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import Resume, Experience, Education, Certificate
from .serializers import (
    ResumeListSerializer,
    ResumeDetailSerializer,
    ResumeCreateSerializer,
    ExperienceSerializer, 
    EducationSerializer, 
    CertificateSerializer
)
from apps.core.models import ActivityLog

class IsSeamanOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow seamen to create and edit resumes.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to seamen
        return request.user and request.user.is_authenticated and request.user.is_seaman
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.seaman == request.user

class ResumeViewSet(viewsets.ModelViewSet):
    """ViewSet for resumes"""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['desired_position', 'total_experience_years', 'availability', 'is_active', 'is_featured']
    search_fields = ['title', 'summary', 'skills', 'languages']
    ordering_fields = ['created_at', 'updated_at', 'total_experience_years', 'desired_salary', 'views_count']
    ordering = ['-created_at']
    permission_classes = [IsSeamanOrReadOnly]
    
    def get_queryset(self):
        """
        Filter resumes based on user type and query parameters
        """
        queryset = Resume.objects.all()
        
        # Apply filtering
        user = self.request.user
        
        # Filter by active status for non-owners
        if not user.is_staff and (self.action == 'list' or self.action == 'retrieve'):
            # Seamen can see their own inactive resumes
            if user.is_seaman:
                queryset = queryset.filter(Q(is_active=True) | Q(seaman=user))
            else:
                queryset = queryset.filter(is_active=True)
        
        # Filter by preferred vessel types
        vessel_type = self.request.query_params.get('vessel_type', None)
        if vessel_type:
            queryset = queryset.filter(preferred_vessel_types__id=vessel_type)
        
        # Filter by years of experience
        min_exp = self.request.query_params.get('min_experience', None)
        if min_exp:
            queryset = queryset.filter(total_experience_years__gte=min_exp)
        
        max_exp = self.request.query_params.get('max_experience', None)
        if max_exp:
            queryset = queryset.filter(total_experience_years__lte=max_exp)
        
        # Filter by salary expectations
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            queryset = queryset.filter(desired_salary__gte=min_salary)
        
        # Filter by availability
        available_from = self.request.query_params.get('available_from', None)
        if available_from:
            queryset = queryset.filter(
                Q(available_from__lte=available_from) | Q(availability='immediate')
            )
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class
        """
        if self.action == 'create':
            return ResumeCreateSerializer
        elif self.action == 'list':
            return ResumeListSerializer
        return ResumeDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to increment view count
        """
        instance = self.get_object()
        
        # Increment view count if the viewer is not the owner
        if request.user != instance.seaman:
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
            
            # Log the activity
            ActivityLog.objects.create(
                user=request.user,
                action='view_resume',
                object_id=instance.id,
                object_type='Resume',
                details={'title': instance.title}
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_resumes(self, request):
        """
        Custom endpoint to list current seaman's resumes
        """
        if not request.user.is_seaman:
            return Response(
                {"detail": "Only seamen can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(seaman=request.user)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Custom endpoint to activate a resume
        """
        resume = self.get_object()
        
        if resume.seaman != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        resume.is_active = True
        resume.save(update_fields=['is_active'])
        
        serializer = self.get_serializer(resume)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Custom endpoint to deactivate a resume
        """
        resume = self.get_object()
        
        if resume.seaman != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        resume.is_active = False
        resume.save(update_fields=['is_active'])
        
        serializer = self.get_serializer(resume)
        return Response(serializer.data)

class ExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for work experience entries"""
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter experiences by resume"""
        resume_id = self.kwargs.get('resume_id')
        return Experience.objects.filter(resume_id=resume_id)
    
    def perform_create(self, serializer):
        """Set the resume when creating a new experience"""
        resume_id = self.kwargs.get('resume_id')
        resume = Resume.objects.get(id=resume_id)
        
        # Check if the user owns the resume
        if resume.seaman != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to add experience to this resume")
        
        serializer.save(resume_id=resume_id)

class EducationViewSet(viewsets.ModelViewSet):
    """ViewSet for education entries"""
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter education by resume"""
        resume_id = self.kwargs.get('resume_id')
        return Education.objects.filter(resume_id=resume_id)
    
    def perform_create(self, serializer):
        """Set the resume when creating a new education entry"""
        resume_id = self.kwargs.get('resume_id')
        resume = Resume.objects.get(id=resume_id)
        
        # Check if the user owns the resume
        if resume.seaman != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to add education to this resume")
        
        serializer.save(resume_id=resume_id)

class CertificateViewSet(viewsets.ModelViewSet):
    """ViewSet for certificate entries"""
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter certificates by resume"""
        resume_id = self.kwargs.get('resume_id')
        return Certificate.objects.filter(resume_id=resume_id)
    
    def perform_create(self, serializer):
        """Set the resume when creating a new certificate"""
        resume_id = self.kwargs.get('resume_id')
        resume = Resume.objects.get(id=resume_id)
        
        # Check if the user owns the resume
        if resume.seaman != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to add certificates to this resume")
        
        serializer.save(resume_id=resume_id)