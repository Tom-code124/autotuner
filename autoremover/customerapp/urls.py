from django.urls import path

from .views  import *

urlpatterns = [
    path('', dashboard_page, name="Dashboard"),
    path('winols_modal/', winols_modal, name='WinOLS Modal'),
    path('pricing_modal/', pricing_modal, name="File Pricing"),
    path('price_options_modal', price_options_modal, name="Price Options Modal"),
    path('login/', login_page, name="Log-in"),
    path('authenticate', authenticate, name="Log-in Try"),
    path('create_account', create_account, name="Create Account"),
    path('dtc_search/', dtc_search_page, name='DTC Search'),
    path('dtc_search/dtc_search_modal', dtc_search_modal, name='DTC Search Modal'),
    path('knowledgebase/', knowledgebase_page, name='Knowledgebase'),
    path('knowledgebase/knowledge_modal', knowledge_modal, name='Knowledge Modal')
]
