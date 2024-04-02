from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', signup_page, name="Signup"),
    path('login/', login_page, name="Login"),
    path('logout/', logout_view, name="Logout"),
    path('deposit_modal/', deposit_modal, name="deposit_modal"),
    path('', dashboard_page, name="Dashboard"),
    path('pricing_modal/', pricing_modal, name="File Pricing"),
    path('price_options_modal', price_options_modal, name="Price Options Modal"),
    path('files/', files_page, name="Files"),
    path('files/requested_files', requested_files_modal, name="Requested Files"),
    path('files/bought_files', bought_files_modal, name="Bought Files"),
    path('upload/', upload_page, name="Upload"),
    path('upload/get_vehicle/', vehicle_select_modal, name="Vehicle Select Modal"),
    path('upload/get_process_options/', process_options_modal, name="Vehicle Process Options Modal"),
    path('vehicle_data/', vehicle_data_page, name="Vehicle Data"),
    path('shop/', shop_page, name="Shop"),
    path('shop/get_products', shop_modal, name="Shop Modal"),
    path('shop/product_modal', product_modal, name="Product Modal"),
    path('shop/purchase_file/', purchase_file, name="purchase_file"),
    path('winols_modal/', winols_modal, name='WinOLS Modal'),
    path('expense_history/', expense_history_page, name="Expense History"),
    path('expense_history/expenses_modal', expenses_modal, name="Expenses Modal"),
    path('dtc_search/', dtc_search_page, name='DTC Search'),
    path('dtc_search/dtc_search_modal', dtc_search_modal, name='DTC Search Modal'),
    path('bosch_search/', bosch_search_page, name='Bosch Search'),
    path('bosch_search/bosch_modal', bosch_modal, name='Bosch Search Modal'),
    path('knowledgebase/', knowledgebase_page, name='Knowledgebase'),
    path('knowledgebase/knowledge_modal', knowledge_modal, name='Knowledge Modal'),
    path('settings/', settings_page, name='Settings'),
    path('download', download_file, name='download')
]
