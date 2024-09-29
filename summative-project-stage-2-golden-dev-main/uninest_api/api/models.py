from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

# This file contains the models for the UniNest API, representing the core entities of the student housing system.

class Building(models.Model):
    """
    Represents a building in the student housing system.
    """
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Specify default ordering for Building objects by name

class Room(models.Model):
    """
    Represents a room within a building, including its capacity and occupancy status.
    """
    room_number = models.CharField(max_length=10)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.building.name} - Room {self.room_number}"

    def is_at_capacity(self):
        """
        Checks if the room is at full capacity based on the number of residents.
        """
        return self.residents.count() >= self.capacity

    class Meta:
        ordering = ['building', 'room_number']

class Resident(models.Model):
    """
    Represents a resident (student) living in the housing system.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']

class MaintenanceRequest(models.Model):
    """
    Represents a maintenance request for a specific room.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance Request for {self.room} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']  # Order maintenance requests by creation date, most recent first

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('administrator', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
