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
    search_fields = ["key"]


class FloorRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "building"]
    search_fields = ["key", "name", "building__key"]


class NurseRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name"]
    search_fields = ["key", "name"]

class RoomRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "floor", "nurse"]
    search_fields = ["key", "name", "floor__name", "nurse__name"]

class BedRecordsAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "status", "room"]
    search_fields = ["key", "name", "status", "room__name"]



admin.site.register(BuildingRecords, BuildingRecordsAdmin)
admin.site.register(FloorRecords, FloorRecordsAdmin)
admin.site.register(NurseRecords, NurseRecordsAdmin)
admin.site.register(RoomRecords, RoomRecordsAdmin)
admin.site.register(BedRecords, BedRecordsAdmin)