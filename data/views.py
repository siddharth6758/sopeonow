import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm
from .helpers import handle_keys, upload_data_to_db

def home(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        data = pd.read_csv(csv_file)
        data = data.dropna()
        # print(data.columns)
        data = handle_keys(data, "BUILDINGKEY")
        data = handle_keys(data, "FLOORKEY")
        data = handle_keys(data, "NURSEKEY")
        data = handle_keys(data, "ROOMKEY")
        data = handle_keys(data, "BEDKEY")
        upload_data_to_db(data)
        return render(request, 'dashboard.html', context={
            "data":data.to_html()
        })
    else:
        csv_form = CSVUploadForm()
        return render(request,'index.html', context={
            "input_form": csv_form
        })