from django.test import TestCase
from .models import Building, Room, Resident, MaintenanceRequest

# Create tests here.

class BuildingModelTest(TestCase):
    def setUp(self):
        Building.objects.create(name="Test Building", address="123 Test St", total_rooms=10)

    def test_building_creation(self):
        building = Building.objects.get(name="Test Building")
        self.assertEqual(building.total_rooms, 10)

# Add more tests for other models and views
