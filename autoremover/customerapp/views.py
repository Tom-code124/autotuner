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
    monthly_file_nums = [1, 0, 3, 7, 0, 9, 4, 2, 0, 11, 4, 7]
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    max_num = max(monthly_file_nums)
    
    monthly_data = []
    for i in range(12):
        m = {
            'name': months[i],
            'file_num': monthly_file_nums[i],
            'percent': monthly_file_nums[i] * 100 / max_num,
        }
        monthly_data.append(m)

    context = {
        'page_title': 'DTC Search',
        'styling_files': ["dashboard.css"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'files_submitted_data': {
            'today': 1,
            'week': 3,
            'month': monthly_file_nums[-1],
            'monthly_data': monthly_data
        }
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

def knowledgebase_page(request):
    knowledge_data = [
        {
            'title': 'Adblue Solutions',
            'desc': 'You can find Adblue Solutions in this page',
            'inner_data': [
                {
                    'sub_title': "AGRALE",
                    'bullets': [
                        'BOSCH EDC7UC31 -  Adblue Ecu and Pump must be disconnected '
                    ]
                },
                {
                    'sub_title': "ASTRA",
                    'bullets': [
                        'BOSCH EDC7UC31 - Adblue ECU to be unplugged',
                        'BOSCH EDC17CV41 - Adblue ECU and Pump to be unplugged'
                    ]
                }
            ]
        },
        {
            'title': 'MED17 VCDS Logging profiles',
            'desc': '<a href="https://drive.tiny.cloud/1/8lqf2m98sdocyt5hqrl8t0s6pir4vto88le9axrfsvxajoep/324197e6-1ac1-46a2-b358-13d3d436756c">Audi a5 - med171 - gen logs.zip</a>\n\nGeneral logging profiles for the Med17.1 Vag ECU - VCDS Advanced - Open the unzipped file and it will populate the logging profile for you.\nGeneral sweep 1500rpm - redline needed for full scope, highest gear possible for more info'
        },
        {
            'title': 'EGR OFF Solutions',
            'inner_data': [
                {
                    'sub_title': 'ALFA ROMEO',
                    'bullets': [
                        'BOSCH EDC15C7 - Actuator to be unplugged',
                        'BOSCH EDC17C69',
                        'MARELLI MJ8'
                    ]
                },
                {
                    'sub_title': 'Aston Martin',
                    'bullets': [
                        'VISTEON EECVI  - Actuator to be unplugged'
                    ]
                }
            ]
        }
    ]

    context = {
        'page_title': 'Knowledgebase',
        'styling_files': ["knowledgebase.css"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'knowledge_data': knowledge_data
    }
    return render(request, "pages/knowledgebase.html", context)
