from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from .models import Conversation, Message, Notification, EmailSubscription
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    NotificationSerializer,
    EmailSubscriptionSerializer
)
from apps.core.models import ActivityLog

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow participants to view and send messages in a conversation.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        return obj.participants.filter(id=request.user.id).exists()

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations"""
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter conversations to those the user is a participant in"""
        return Conversation.objects.filter(participants=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return ConversationCreateSerializer
        elif self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to mark messages as read
        """
        instance = self.get_object()
        
        # Mark messages as read if not sender
        Message.objects.filter(
            conversation=instance,
            is_read=False
        ).exclude(
            sender=request.user
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        # Return conversation with messages
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Custom endpoint to send a message in a conversation
        """
        conversation = self.get_object()
        
        # Create the serializer with conversation context
        serializer = MessageCreateSerializer(
            data=request.data,
            context={'request': request, 'conversation': conversation}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action='message',
            object_id=conversation.id,
            object_type='Conversation'
        )
        
        # Return the created message
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notifications"""
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter notifications to those for the current user"""
        return Notification.objects.filter(recipient=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=['is_read', 'read_at'])
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({"status": "All notifications marked as read"})

class EmailSubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for email subscription preferences"""
    serializer_class = EmailSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter email subscriptions to those for the current user"""
        return EmailSubscription.objects.filter(user=self.request.user)
    
    def list(self, request):
        """Get user's email preferences"""
        # Get or create email preferences
        email_prefs, created = EmailSubscription.objects.get_or_create(user=request.user)
        
        serializer = self.get_serializer(email_prefs)
        return Response(serializer.data)
    
    def create(self, request):
        """Redirect to update instead of create"""
        return self.update(request)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """Update email preferences"""
        # Get or create email preferences
        email_prefs, created = EmailSubscription.objects.get_or_create(user=request.user)
        
        serializer = self.get_serializer(email_prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)