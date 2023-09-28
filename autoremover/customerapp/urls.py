from django.urls import path

from .views  import *

urlpatterns = [
    path('login/', login_page, name="Log-in"),
    path('authenticate', authenticate, name="Log-in Try"),
    path('create_account', create_account, name="Create Account"),
    path('', dashboard_page, name="Dashboard"),
    path('pricing_modal/', pricing_modal, name="File Pricing"),
    path('price_options_modal', price_options_modal, name="Price Options Modal"),
    path('files/', files_page, name="Your Files"),
    path('files/requested_files', requested_files_modal, name="Requested Files"),
    path('winols_modal/', winols_modal, name='WinOLS Modal'),
    path('expense_history/', expense_history_page, name="Expense History"),
    path('expense_history/expenses_modal', expenses_modal, name="Expenses Modal"),
    path('dtc_search/', dtc_search_page, name='DTC Search'),
    path('dtc_search/dtc_search_modal', dtc_search_modal, name='DTC Search Modal'),
    path('bosch_search/', bosch_search_page, name='Bosch Search'),
    path('bosch_search/bosch_modal', bosch_modal, name='Bosch Search'),
    path('knowledgebase/', knowledgebase_page, name='Knowledgebase'),
    path('knowledgebase/knowledge_modal', knowledge_modal, name='Knowledge Modal')
]
