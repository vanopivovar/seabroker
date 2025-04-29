from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import ProfileViewSet, DocumentViewSet

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Direct endpoints for current user profile
    path('me/', ProfileViewSet.as_view({'get': 'me', 'put': 'update_me', 'patch': 'update_me'}), name='current-user'),
]