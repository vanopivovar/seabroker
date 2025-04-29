from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import Application, ApplicationStatusHistory
from .serializers import (
    ApplicationListSerializer,
    ApplicationDetailSerializer, 
    ApplicationCreateSerializer,
    ApplicationStatusUpdateSerializer,
    ApplicationStatusHistorySerializer
)
from apps.core.models import ActivityLog

class IsOwnerOrEmployerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow seamen to create applications and
    owners or employers to view and modify them.
    """
    def has_permission(self, request, view):
        # Allow authenticated users to create applications
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.is_seaman
        
        # Allow authenticated users to list/retrieve
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True
        
        # Allow the applicant to see their own applications
        if obj.applicant == request.user:
            return True
        
        # Allow the employer to see applications for their vacancies
        if obj.vacancy.employer == request.user:
            # Employers can update application status
            if request.method in ['PUT', 'PATCH']:
                return True
            
            # Employers can view applications
            return request.method in permissions.SAFE_METHODS
        
        # Deny access to other users
        return False

class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for applications"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'vacancy', 'resume']
    ordering_fields = ['created_at', 'updated_at', 'status_changed_at']
    ordering = ['-created_at']
    permission_classes = [IsOwnerOrEmployerOrReadOnly]
    
    def get_queryset(self):
        """
        Filter applications based on user type
        """
        user = self.request.user
        
        # Staff can see all applications
        if user.is_staff:
            return Application.objects.all()
        
        # Seamen can see their own applications
        if user.is_seaman:
            return Application.objects.filter(applicant=user)
        
        # Employers can see applications for their vacancies
        if user.is_employer:
            return Application.objects.filter(vacancy__employer=user)
        
        # Other users can't see any applications
        return Application.objects.none()
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class
        """
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'update_status':
            return ApplicationStatusUpdateSerializer
        elif self.action == 'list':
            return ApplicationListSerializer
        return ApplicationDetailSerializer
    
    def perform_create(self, serializer):
        """
        Create a new application and log activity
        """
        application = serializer.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=self.request.user,
            action='apply',
            object_id=application.vacancy.id,
            object_type='Vacancy',
            details={'vacancy_title': application.vacancy.title}
        )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Custom endpoint to update application status
        """
        application = self.get_object()
        serializer = self.get_serializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return the updated application using the detail serializer
        detail_serializer = ApplicationDetailSerializer(application)
        return Response(detail_serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """
        Custom endpoint to list current user's applications
        """
        if not request.user.is_seaman:
            return Response(
                {"detail": "Only seamen can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(applicant=request.user)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def received_applications(self, request):
        """
        Custom endpoint to list applications received by an employer
        """
        if not request.user.is_employer:
            return Response(
                {"detail": "Only employers can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(vacancy__employer=request.user)
        
        # Filter by status if provided
        status_param = request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by vacancy if provided
        vacancy_param = request.query_params.get('vacancy_id', None)
        if vacancy_param:
            queryset = queryset.filter(vacancy_id=vacancy_param)
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)