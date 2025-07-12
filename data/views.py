import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm
from .utils import BED_STATUS
from .helpers import handle_keys, upload_data_to_db, get_dashboard_data

def home(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        data = pd.read_csv(csv_file)
        has_records = False
        data = data.dropna()
        data = handle_keys(data, "BUILDINGKEY")
        data = handle_keys(data, "FLOORKEY")
        data = handle_keys(data, "NURSEKEY")
        data = handle_keys(data, "ROOMKEY")
        data = handle_keys(data, "BEDKEY")
        upload_data_to_db(data)
        data_rec = get_dashboard_data()
        for val in data_rec.values():
            if val:
                has_records = True
        return render(request, 'dashboard.html', context={
            "data": data_rec,
            "bed_status": dict(BED_STATUS),
            "has_records": has_records
        })
    else:
        csv_form = CSVUploadForm()
        return render(request,'index.html', context={
            "input_form": csv_form
        })

def show_previous_data(request):
    data_rec = get_dashboard_data()
    has_records = False
    for val in data_rec.values():
        if val:
            has_records = True
    return render(request, 'dashboard.html', context={
        "data": data_rec,
        "bed_status": dict(BED_STATUS),
        "has_records": has_records
    })