from django.db import models
from .utils import BED_STATUS

class BuildingRecords(models.Model):
    key = models.IntegerField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.key}"

    class Meta:
        verbose_name = 'BuildingRecord'
        verbose_name_plural = 'BuildingRecords'

class FloorRecords(models.Model):
    key = models.IntegerField(max_length=10, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    building = models.ForeignKey(BuildingRecords, on_delete=models.CASCADE, related_name='floors')

    def __str__(self):
        return f"{self.name}-{self.building.key}"

    class Meta:
        verbose_name = 'FloorRecord'
        verbose_name_plural = 'FloorRecords'

class NurseRecords(models.Model):
    key = models.IntegerField(max_length=10)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.key}-{self.name}"

    class Meta:
        verbose_name = 'NurseRecord'
        verbose_name_plural = 'NurseRecords'
        unique_together = ["key", "name"]

class RoomRecords(models.Model):
    key = models.IntegerField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    floor = models.ForeignKey(FloorRecords, on_delete=models.CASCADE, related_name='rooms')
    nurse = models.ForeignKey(NurseRecords, on_delete=models.SET_NULL, null=True, blank=True, related_name='rooms')

    def __str__(self):
        return f"{self.name}-{self.floor.name}"

    class Meta:
        verbose_name = 'RoomRecord'
        verbose_name_plural = 'RoomRecords'

class BedRecords(models.Model):
    key = models.IntegerField(max_length=10, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=BED_STATUS, default="nan")
    room = models.ForeignKey(RoomRecords, on_delete=models.CASCADE, related_name='beds')

    def __str__(self):
        return f"{self.name}-{self.room.name}"

    class Meta:
        verbose_name = 'BedRecord'
        verbose_name_plural = 'BedRecords'