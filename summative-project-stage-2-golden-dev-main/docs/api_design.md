from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_rooms = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.building.name} - Room {self.room_number}"

class Resident(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Ensure email is unique
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)  # Allow null for unassigned residents

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance Request for {self.room} - {self.status}"
