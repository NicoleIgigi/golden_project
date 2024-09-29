from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Building, Room, Resident, MaintenanceRequest
from .serializers import BuildingSerializer, RoomSerializer, ResidentSerializer, MaintenanceRequestSerializer
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'administrator'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class BuildingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Building instances.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RoomFilter
    search_fields = ['room_number']
    ordering_fields = ['room_number', 'capacity']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('min_capacity', openapi.IN_QUERY, description="Minimum room capacity", type=openapi.TYPE_INTEGER),
            openapi.Parameter('max_capacity', openapi.IN_QUERY, description="Maximum room capacity", type=openapi.TYPE_INTEGER),
        ],
        responses={200: RoomSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        Get a list of all rooms.
        This endpoint supports filtering by capacity, searching by room number, and ordering.
        """
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Override to ensure the room's building total_rooms is not exceeded.
        """
        building = serializer.validated_data['building']
        # Check if the building has reached its maximum room capacity
        if building.rooms.count() >= building.total_rooms:
            raise serializers.ValidationError("Building has reached its maximum room capacity.")
        serializer.save()

class ResidentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Resident instances.
    """
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room', 'room__building']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name']

    def perform_create(self, serializer):
        """
        Override to update the room's occupied status when creating a new resident.
        """
        resident = serializer.save()
        if resident.room:
            # Check if the room is at full capacity
            if resident.room.is_at_capacity():
                raise serializers.ValidationError("Room is at full capacity.")
            # Update the room's occupied status
            resident.room.is_occupied = True
            resident.room.save()

    def perform_update(self, serializer):
        """
        Override to handle room changes when updating a resident.
        """
        old_room = self.get_object().room
        resident = serializer.save()
        if old_room != resident.room:
            if old_room:
                # Update the old room's occupied status
                old_room.is_occupied = old_room.residents.exists()
                old_room.save()
            if resident.room:
                # Check if the new room is at full capacity
                if resident.room.is_at_capacity():
                    raise serializers.ValidationError("New room is at full capacity.")
                # Update the new room's occupied status
                resident.room.is_occupied = True
                resident.room.save()

    @action(detail=True, methods=['post'])
    def assign_room(self, request, pk=None):
        resident = self.get_object()
        room_id = request.data.get('room_id')
        if not room_id:
            return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = Room.objects.get(id=room_id)
            if room.is_at_capacity():
                return Response({"error": "Room is at capacity"}, status=status.HTTP_400_BAD_REQUEST)
            resident.room = room
            resident.save()
            return Response({"success": "Room assigned successfully"})
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing MaintenanceRequest instances.
    """
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer

    def perform_create(self, serializer):
        """
        Override to ensure the maintenance request is associated with an occupied room.
        """
        room = serializer.validated_data['room']
        # Check if the room is occupied before creating a maintenance request
        if not room.is_occupied:
            raise serializers.ValidationError("Cannot create maintenance request for unoccupied room.")
        serializer.save()

# Asynchronous Programming Potential:
# - Long-running tasks like generating reports could benefit from asynchronous execution.
# - Real-time notifications for maintenance requests could use asynchronous methods.
# - Bulk operations (e.g., assigning multiple rooms) could be handled asynchronously.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import YourModel
from .serializers import YourModelSerializer

@api_view(['GET'])
def cached_view(request):
    cache_key = 'your_cache_key'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # If data is not in cache, fetch it and cache it
        queryset = YourModel.objects.all()
        serializer = YourModelSerializer(queryset, many=True)
        cached_data = serializer.data
        cache.set(cache_key, cached_data, timeout=3600)  # Cache for 1 hour
    
    return Response(cached_data)

# You can add a student-specific view like this:
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def student_room_view(request):
    try:
        resident = Resident.objects.get(email=request.user.email)
        if resident.room:
            serializer = RoomSerializer(resident.room)
            return Response(serializer.data)
        else:
            return Response({"message": "You are not assigned to a room yet."}, status=status.HTTP_404_NOT_FOUND)
    except Resident.DoesNotExist:
        return Response({"message": "Resident profile not found."}, status=status.HTTP_404_NOT_FOUND)