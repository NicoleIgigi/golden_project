from rest_framework import serializers
from .models import Building, Room, Resident, MaintenanceRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class BuildingSerializer(serializers.ModelSerializer):
    # Ensure total_rooms is a positive integer
    total_rooms = serializers.IntegerField(min_value=1)
    
    class Meta:
        model = Building
        fields = ['id', 'name', 'address', 'total_rooms']

class RoomSerializer(serializers.ModelSerializer):
    # Include the building name as a read-only field
    building_name = serializers.CharField(source='building.name', read_only=True)
    # Ensure capacity is a positive integer
    capacity = serializers.IntegerField(min_value=1)
    # Add a read-only field to check if the room is at capacity
    is_at_capacity = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'building', 'building_name', 'capacity', 'is_occupied', 'is_at_capacity']

class ResidentSerializer(serializers.ModelSerializer):
    # Include the room number as a read-only field
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    
    class Meta:
        model = Resident
        fields = ['id', 'first_name', 'last_name', 'email', 'room', 'room_number']

    def validate_room(self, value):
        # Check if the room is at capacity before assigning a resident
        if value and value.is_at_capacity():
            raise serializers.ValidationError("This room is at full capacity.")
        return value

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    # Include the room number as a read-only field
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    # Include the human-readable status as a read-only field
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'room', 'room_number', 'description', 'status', 'status_display', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']