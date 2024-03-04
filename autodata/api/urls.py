from django.urls import path

from .views import *

urlpatterns = [
    path('vehicle_select/', vehicle_select_api, name="Vehicle Select API"),
]
