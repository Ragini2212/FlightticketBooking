from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    name = models.CharField(max_length=10, unique=True)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    seat_count = models.IntegerField()
    
    def __str__(self):
        return self.name



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.IntegerField()
    
    def __str__(self):
        return self.user.username
