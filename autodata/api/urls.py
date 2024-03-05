from django.urls import path

from .views import *

urlpatterns = [
    path('vehicle_select/', vehicle_select_api, name="Vehicle Select API"),
    path('dtc_search/', dtc_search_api, name="DTC Search API"),
    path('bosch_search/', bosch_search_api, name="Bosch Search API"),
]
