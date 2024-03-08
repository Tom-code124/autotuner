from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_page, name="Panel Login"),
    path('logout/', logout_view, name="Panel Logout"),
    path('', pricing_page, name="Panel Pricing"),
]
