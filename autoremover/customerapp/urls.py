from django.urls import path

from .views  import *

urlpatterns = [
    path('', dashboard_page, name="Dashboard"),
    path('login/', login_page, name="Log-in"),
    path('dtc_search/', dtc_search_page, name='DTC Search'),
    path('knowledgebase/', knowledgebase_page, name='Knowledgebase')
]