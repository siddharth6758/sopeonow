from django.db.models import Count
from django.db.models import Q
from .models import (
    BuildingRecords,
    FloorRecords,
    NurseRecords,
    RoomRecords,
    BedRecords
)
from .utils import BED_STATUS

def remove_invalid_str_keys(value):
    try:
        int(value)
        return True
    except Exception:
        return False

def handle_keys(df, column):
    return df[df[column].apply(remove_invalid_str_keys)]

def upload_building_records(data):
    existing_keys = BuildingRecords.objects.filter(key__in=data.unique()).values_list("key",flat=True)

    building_records = [
        BuildingRecords(key=int(value))
        for value in data.unique() if value not in existing_keys
    ]
    BuildingRecords.objects.bulk_create(building_records)


def upload_floor_records(data):
    key_list = data["FLOORKEY"].unique()
    floor_query = FloorRecords.objects.filter(key__in=key_list)
    existing_keys = floor_query.values_list("key",flat=True)
    existing_object_map = {obj.key: obj for obj in floor_query}

    floor_records = []
    floor_records_update = []

    for row in data.itertuples():
        building_obj,_ = BuildingRecords.objects.get_or_create(key=int(row.BUILDINGKEY))
        if int(row.FLOORKEY) in existing_keys:
            floor_instance = existing_object_map[int(row.FLOORKEY)]
            floor_instance.name = row.FLOORNAME
            floor_instance.building = building_obj
            floor_records_update.append(floor_instance)
        else:
            floor_records.append(
                FloorRecords(key=int(row.FLOORKEY), name=row.FLOORNAME, building=building_obj)
            )

    if floor_records:
        FloorRecords.objects.bulk_create(floor_records)
    elif floor_records_update:
        FloorRecords.objects.bulk_update(floor_records_update,["name", "building"])


def upload_nursing_records(data):
    key_list = data["NURSEKEY"].unique()
    existing_keys = NurseRecords.objects.filter(key__in=key_list).values_list("key",flat=True)

    nursing_records = [
        NurseRecords(key=int(row.NURSEKEY), name=row.NURSENAME)
        for row in data.itertuples() if int(row.NURSEKEY) not in existing_keys
    ]
    NurseRecords.objects.bulk_create(nursing_records)


def upload_room_records(data):
    key_list = data["ROOMKEY"].unique()
    room_query = RoomRecords.objects.filter(key__in=key_list)
    existing_keys = room_query.values_list("key",flat=True)
    existing_object_map = {obj.key: obj for obj in room_query}

    room_records = []
    room_records_update = []

    for row in data.itertuples():
        floor_obj,_ = FloorRecords.objects.get_or_create(key=int(row.FLOORKEY))
        nurse_obj,_ = NurseRecords.objects.get_or_create(key=int(row.NURSEKEY), name=row.NURSENAME)
        if int(row.ROOMKEY) in existing_keys:
            room_instance = existing_object_map[int(row.ROOMKEY)]
            room_instance.name = row.ROOMNAME
            room_instance.floor = floor_obj
            room_instance.nurse = nurse_obj
            room_records_update.append(room_instance)
        else:
            room_records.append(
                RoomRecords(key=int(row.ROOMKEY), name=row.ROOMNAME, floor=floor_obj, nurse=nurse_obj)
            )

    if room_records:
        RoomRecords.objects.bulk_create(room_records)
    elif room_records_update:
        RoomRecords.objects.bulk_update(room_records_update,["name", "floor", "nurse"])


def upload_bed_records(data):
    key_list = data["BEDKEY"].unique()
    bed_query = BedRecords.objects.filter(key__in=key_list)
    existing_keys = bed_query.values_list("key",flat=True)
    existing_object_map = {obj.key: obj for obj in bed_query}

    floor_records = []
    floor_records_update = []

    for row in data.itertuples():
        room_obj,_ = RoomRecords.objects.get_or_create(key=int(row.ROOMKEY))
        status_key = next((key for key, value in BED_STATUS if value == row.BEDSTATUS), None)
        if int(row.BEDKEY) in existing_keys:
            floor_instance = existing_object_map[int(row.BEDKEY)]
            floor_instance.name = row.BEDNAME
            floor_instance.status = status_key
            floor_instance.room = room_obj
            floor_records_update.append(floor_instance)
        else:
            floor_records.append(
                BedRecords(key=int(row.BEDKEY), name=row.BEDNAME, status=status_key, room=room_obj)
            )

    if floor_records:
        BedRecords.objects.bulk_create(floor_records)
    elif floor_records_update:
        BedRecords.objects.bulk_update(floor_records_update,["name", "status","room"])


def upload_data_to_db(data):
    upload_building_records(data["BUILDINGKEY"])
    upload_floor_records(data[["BUILDINGKEY","FLOORKEY","FLOORNAME"]].drop_duplicates())
    upload_nursing_records(data[["NURSEKEY","NURSENAME"]].drop_duplicates())
    upload_room_records(data[["FLOORKEY","NURSEKEY","NURSENAME","ROOMKEY","ROOMNAME"]].drop_duplicates())
    upload_bed_records(data[["ROOMKEY","BEDKEY","BEDNAME","BEDSTATUS"]].drop_duplicates())


def get_dashboard_data():
    data = {}
    nurse_bed_count = NurseRecords.objects.annotate(
        bed_count=Count("rooms__beds")
    ).values_list("key","name","bed_count")

    room_bed_count = RoomRecords.objects.annotate(
        bed_count=Count("beds")
    ).values_list("key","name","bed_count")

    bed_status_count = BedRecords.objects.values("status").annotate(
        bed_count=Count("status")
    ).values_list("status","bed_count")

    total_bed_count = BedRecords.objects.count()
    occupied_bed_count = BedRecords.objects.filter(status__icontains="occupied").count()
    occupied_percentage = round((occupied_bed_count/total_bed_count)*100 if total_bed_count > 0 else 0, 2)

    nurse_occupancy_count = NurseRecords.objects.annotate(
        occupied_count=Count("rooms__beds", filter=Q(rooms__beds__status__icontains="occupied"))
    ).values_list("key","name","occupied_count")

    room_occupancy_count = RoomRecords.objects.annotate(
        occupied_count=Count("beds", filter=Q(beds__status__icontains="occupied"))
    ).values_list("key","name","occupied_count")
    print(room_occupancy_count,end="\n")
    return data