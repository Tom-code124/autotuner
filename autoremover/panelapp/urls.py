from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_page, name="Panel Login"),
    path('logout/', logout_view, name="Panel Logout"),
    path('manage_customers/', customers_page, name="Panel Manage Customers"),
    path('manage_customers/update_customer/', update_customer, name="Panel Update Customer"),
    path('customer_options/', customer_options, name="Panel Customer Options"),
    path('pricing/', pricing_page, name="Panel Pricing"),
    path('pricing/ecu_type_search/', ecu_type_search_modal, name="Panel Ecu Type Search"),
    path('pricing/filter_vehicles/', filter_vehicles_modal, name="Panel Filter Vehicles"),
    path('pricing/make_pricing/', make_pricing_modal, name="Panel Make Pricing"),
]
