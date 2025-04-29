from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet

# Create a router for applications
router = DefaultRouter()
router.register(r'', ApplicationViewSet, basename='application')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]