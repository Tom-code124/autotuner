from django.urls import path

from .views import *

urlpatterns = [
    path('pricing/', pricing_page, name="Panel Pricing"),
]
