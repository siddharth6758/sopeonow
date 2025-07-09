import pandas as pd
from .models import (
    BuildingRecords,
    FloorRecords,
    NurseRecords,
    RoomRecords,
    BedRecords
)

def remove_invalid_str_keys(value):
    try:
        int(value)
        return True
    except Exception:
        return False


def upload_building_records(data):
    existing_keys = BuildingRecords.objects.filter(key__in=data.unique()).values_list("key",flat=True)

    building_records = [
        BuildingRecords(key=int(value))
        for value in data.unique() if value not in existing_keys
    ]
    BuildingRecords.objects.bulk_create(building_records)


def upload_floor_records(data):
    key_list = data["FLOORKEY"].unique()
    existing_keys = FloorRecords.objects.filter(key__in=key_list).values_list("key",flat=True)
    existing_object_map = {obj.key: obj for obj in FloorRecords.objects.filter(key__in=key_list)}

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

#['BUILDINGKEY', 'FLOORKEY', 'FLOORNAME', 'NURSEKEY', 'NURSENAME', 'ROOMKEY', 'ROOMNAME', 'BEDKEY', 'BEDNAME', 'BEDSTATUS']

def handle_keys(df, column):
    return df[df[column].apply(remove_invalid_str_keys)]


def upload_data_to_db(data):
    upload_building_records(data["BUILDINGKEY"])
    upload_floor_records(data[["BUILDINGKEY","FLOORKEY","FLOORNAME"]].drop_duplicates())
    upload_nursing_records(data[["NURSEKEY","NURSENAME"]].drop_duplicates())
    upload_room_records(data[["FLOORKEY","NURSEKEY","NURSENAME","ROOMKEY","ROOMNAME"]].drop_duplicates())