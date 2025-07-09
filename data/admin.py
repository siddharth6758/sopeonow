from django.contrib import admin
from .models import (
    BuildingRecords,
    FloorRecords,
    NurseRecords,
    RoomRecords,
    BedRecords
)
class BuildingRecordsAdmin(admin.ModelAdmin):
    list_display = ["id", "key"]


class FloorRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "building"]


class NurseRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name"]

class RoomRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "floor", "nurse"]

class BedRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "status", "room"]



admin.site.register(BuildingRecords, BuildingRecordsAdmin)
admin.site.register(FloorRecords, FloorRecordsAdmin)
admin.site.register(NurseRecords, NurseRecordsAdmin)
admin.site.register(RoomRecords, RoomRecordsAdmin)
admin.site.register(BedRecords, BedRecordsAdmin)