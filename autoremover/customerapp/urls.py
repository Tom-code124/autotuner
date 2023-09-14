from django.urls import path

from .views  import *

urlpatterns = [
    path('dtc_search/', dtc_search, name='DTC Search'),
]