from django.urls import path

from .views  import *

urlpatterns = [
    path('', dashboard_page, name="Dashboard"),
    path('pricing_modal/', pricing_modal, name="File Pricing"),
    path('price_options_modal', price_options_modal, name="Price Options Modal"),
    path('login/', login_page, name="Log-in"),
    path('dtc_search/', dtc_search_page, name='DTC Search'),
    path('knowledgebase/', knowledgebase_page, name='Knowledgebase'),
    path('winols_modal/', winols_modal, name='WinOLS Modal'),
    path('knowledgebase/knowledge_modal', knowledge_modal, name='Knowledge Modal')
]