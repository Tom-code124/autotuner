from django.shortcuts import render
from datetime import datetime

# Create your views here.

def login_page(request):
    context = {
        'page_title': 'Log-in',
        'styling_files': ["customer_login.css"],
        }
    return render(request, "pages/customer_login.html", context)

def dashboard_page(request):
    context = {
        'page_title': 'DTC Search',
        'styling_files': ["dashboard.css"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52
    }
    return render(request, "pages/dashboard.html", context)


def dtc_search_page(request):
    dtc_data_amount = 966
    current_page = 2
    dtc_list = [
        {
            'code': 'P0000',
            'desc': 'No fault'
        },
        {
            'code': 'P0001',
            'desc': 'Fuel volume regulator control -circuit open'
        },
        {
            'code': 'P0002',
            'desc': 'Fuel volume regulator control -circuit range/performance'
        },
        {
            'code': 'P0003',
            'desc': 'Fuel volume regulator control -circuit low'
        },
        {
            'code': 'P0004',
            'desc': 'Fuel volume regulator control -circuit high'
        },
        {
            'code': 'P0005',
            'desc': 'Fuel shut -off valve -circuit open'
        },
        {
            'code': 'P0006',
            'desc': 'Fuel shut -off valve -circuit low'
        },
        {
            'code': 'P0007',
            'desc': 'Fuel shut -off valve -circuit high'
        },
        {
            'code': 'P0008',
            'desc': 'Engine position system, bank 1 -engine performance'
        },
        {
            'code': 'P0009',
            'desc': 'Engine position system, bank 2 -engine performance'
        }
    ]
    context = {
        'page_title': 'DTC Search',
        'styling_files': ["dtc_search.css"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'dtc_data': {
            'amount': dtc_data_amount,
            'total_page_num': int(dtc_data_amount / 10) + 1,
            'current_page': current_page,
            'start_index': (current_page - 1) * 10,
            'end_index': current_page * 10 - 1,
            'dtc_list': dtc_list
        }
        }
    return render(request, "pages/dtc_search.html", context)
