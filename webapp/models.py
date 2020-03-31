from django.db import models
from datetime import datetime

class Buildings(models.Model):
    building_name = models.CharField(max_length=30)
    building_id = models.IntegerField()

    def __str__(self):
        return self.building_name
    @property
    def rooms(self):
        return self.rooms_set.all()

class Rooms(models.Model):
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=30, null=True, blank=True)
    room_id = models.IntegerField()

    def __str__(self):
        return self.room_name

    @property
    def devices(self):
        return self.devices_set.all()
class Devices(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=30, null=True, blank=True)
    device_name = models.CharField(max_length=30, null=True, blank=True)
    watts_rating = models.IntegerField(default=0)
    device_id = models.IntegerField()

    def __str__(self):
        return self.device_name
    @property
    def entry(self):
        return self.logging_set.all()

class Logging(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.device_name + " "
