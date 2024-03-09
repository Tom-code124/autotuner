from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_page, name="Panel Login"),
    path('logout/', logout_view, name="Panel Logout"),
    path('customer_options/', customer_options, name="Panel Customer Options"),
    path('', pricing_page, name="Panel Pricing"),
]
