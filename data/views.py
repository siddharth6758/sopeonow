import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CSVUploadForm

def home(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        data = pd.read_csv(csv_file)
        data = data.dropna()
        print('\n\nDATA:\n',data)
        return JsonResponse({})
    else:
        csv_form = CSVUploadForm()
        return render(request,'index.html', context={
            "input_form": csv_form
        })