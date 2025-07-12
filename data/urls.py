from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('stored-data',show_previous_data, name="load_old_data"),
]