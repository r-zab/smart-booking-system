from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (dla {self.capacity} osób)"

class Booking(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Rezerwacja '{self.title}' na {self.resource.name} od {self.start_time} do {self.end_time}"
