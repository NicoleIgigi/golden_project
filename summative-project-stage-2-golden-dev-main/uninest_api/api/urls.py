# Import necessary modules from Django and Django REST framework
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import ViewSets from views.py
from .views import BuildingViewSet, RoomViewSet, ResidentViewSet, MaintenanceRequestViewSet, student_room_view

# Create a router and register our ViewSets with it
router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'residents', ResidentViewSet)
router.register(r'maintenance-requests', MaintenanceRequestViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Include the router-generated URLs in our urlpatterns
    path('', include(router.urls)),
    path('register/', views.register_user, name='register'),
    path('student-room/', student_room_view, name='student-room'),
]
