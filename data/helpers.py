import pandas as pd
from .models import (
    BuildingRecords,
    FloorRecords,
    NurseRecords,
    RoomRecords,
    BedRecords
)

#['BUILDINGKEY', 'FLOORKEY', 'FLOORNAME', 'NURSEKEY', 'NURSENAME', 'ROOMKEY', 'ROOMNAME', 'BEDKEY', 'BEDNAME', 'BEDSTATUS']

def replace_strkeys_with_defaults(value, default=-1):
    try:
        return int(value)
    except Exception:
        return default


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


def upload__records(data):
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


def handle_keys(data):
    data = data.apply(lambda x: replace_strkeys_with_defaults(x, -1))
    return data


def upload_data_to_db(data):
    upload_building_records(data["BUILDINGKEY"])
    upload_floor_records(data[["BUILDINGKEY","FLOORKEY","FLOORNAME"]].drop_duplicates())
    upload_nursing_records(data[["NURSEKEY","NURSENAME"]].drop_duplicates())