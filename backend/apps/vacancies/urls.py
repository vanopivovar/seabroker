from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VesselTypeViewSet, PositionViewSet, VacancyViewSet

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'vessel-types', VesselTypeViewSet, basename='vessel-type')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'', VacancyViewSet, basename='vacancy')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]