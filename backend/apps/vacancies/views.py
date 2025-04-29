from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import VesselType, Position, Vacancy
from .serializers import (
    VesselTypeSerializer,
    PositionSerializer, 
    VacancyListSerializer,
    VacancyDetailSerializer,
    VacancyCreateSerializer
)
from apps.core.models import ActivityLog
from seajobs.schema import auth_required, paginated_response

class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employers to create and edit vacancies.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to employers
        return request.user and request.user.is_authenticated and request.user.is_employer

class VesselTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for vessel types"""
    queryset = VesselType.objects.all()
    serializer_class = VesselTypeSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        """
        Override permissions to allow any user to list and retrieve
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class PositionViewSet(viewsets.ModelViewSet):
    """ViewSet for job positions"""
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        """
        Override permissions to allow any user to list and retrieve
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class VacancyViewSet(viewsets.ModelViewSet):
    """ViewSet for vacancies"""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['position', 'vessel_type', 'contract_type', 'experience_level', 'is_active', 'is_featured']
    search_fields = ['title', 'description', 'requirements', 'location', 'vessel_name']
    ordering_fields = ['created_at', 'updated_at', 'salary_min', 'salary_max', 'experience_years', 'views_count']
    ordering = ['-created_at']
    permission_classes = [IsEmployerOrReadOnly]
    
    def get_queryset(self):
        """
        Filter vacancies based on user type and query parameters
        """
        queryset = Vacancy.objects.all()
        
        # Apply filtering
        user = self.request.user
        
        # Filter by active status for non-owners
        if not user.is_staff and (self.action == 'list' or self.action == 'retrieve'):
            # Employers can see their own inactive vacancies
            if user.is_employer:
                queryset = queryset.filter(Q(is_active=True) | Q(employer=user))
            else:
                queryset = queryset.filter(is_active=True)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by salary range
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        
        max_salary = self.request.query_params.get('max_salary', None)
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)
        
        # Filter by date
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        
        # Filter by application deadline
        deadline_after = self.request.query_params.get('deadline_after', None)
        if deadline_after:
            queryset = queryset.filter(
                Q(application_deadline__gte=deadline_after) | Q(application_deadline__isnull=True)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class
        """
        if self.action == 'create':
            return VacancyCreateSerializer
        elif self.action == 'list':
            return VacancyListSerializer
        return VacancyDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to increment view count
        """
        instance = self.get_object()
        
        # Increment view count if the viewer is not the owner
        if request.user != instance.employer:
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
            
            # Log the activity
            ActivityLog.objects.create(
                user=request.user,
                action='view_vacancy',
                object_id=instance.id,
                object_type='Vacancy',
                details={'title': instance.title}
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_vacancies(self, request):
        """
        Custom endpoint to list current employer's vacancies
        """
        if not request.user.is_employer:
            return Response(
                {"detail": "Only employers can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.get_queryset().filter(employer=request.user)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Custom endpoint to activate a vacancy
        """
        vacancy = self.get_object()
        
        if vacancy.employer != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        vacancy.is_active = True
        vacancy.save(update_fields=['is_active'])
        
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Custom endpoint to deactivate a vacancy
        """
        vacancy = self.get_object()
        
        if vacancy.employer != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        vacancy.is_active = False
        vacancy.save(update_fields=['is_active'])
        
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data)

    @auth_required()
    @paginated_response()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @auth_required()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @auth_required()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @auth_required()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @auth_required()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)