from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, NotificationViewSet, EmailSubscriptionViewSet

# Create a router for conversations and notifications
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'email-preferences', EmailSubscriptionViewSet, basename='email-preferences')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]