from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from urllib.parse import unquote
import math

# Create your views here.

def login_page(request, status="normal"):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.POST.get('next') if request.POST.get('next') else "/app/"
            return redirect(redirect_url)
    
    context = {
        'page_title': 'Log-in',
        'styling_files': ["customer_login.css"],
        'script_files': ["customer_login.js"],
        }
    
    status = request.GET.get('status')

    context["display_login_form"] = "block"
    context["display_signup_form"] = "none"
    
    if status == "login_error":
        context["login_error_message"] = "Wrong email or password"

    if status == "signup_error":
        wrong_data = request.GET.get('wrong')
        context["signup_error_message"] = "This " + wrong_data + " is already being used by another account!"
        context["display_login_form"] = "none"
        context["display_signup_form"] = "block"

    return render(request, "pages/customer_login.html", context)

def logout_view(request):
    logout(request)
    return redirect('/app/login/')

def create_account(request):
    if request.method == "POST":
        emails = [
            "test@test.com",
            "test1@test1.com",
            "test2@test2.com"
        ]

        phones = [
            "123",
            "123456"
        ]
        
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not email in emails:
            if not phone in phones:
                return redirect("/app/")
            else:
                return redirect("/app/login?status=signup_error&wrong=phone")
        else:
                return redirect("/app/login?status=signup_error&wrong=email")

"""
def authenticate(request):
    if request.method == "POST":
        users = {
            "test@test.com": "test",
            "test1@test1.com": "test1",
            "test2@test2.com": "test2"
        }

        email = request.POST.get('email')
        password = request.POST.get('password')
        if email in list(users.keys()):
            if users[email] == password:
                return redirect("/app/")
            
        return redirect('/app/login?status=login_error')
"""
    
@login_required
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

    new_know_data = [
        {
            'date': '22.11.2023',
            'desc': 'Scania S500-770 DC13-16 EMS10 SCR'
        },
        {
            'date': '19.11.2023',
            'desc': 'Scania S500-770 DC13-16 EMS10 SCR off EGR on original new gearbox and sme other fixes with some updates'
        },
        {
            'date': '10.10.2023',
            'desc': 'Scania S500-770 DC13-16 EMS10 SCR off'
        },
        {
            'date': '22.09.2023',
            'desc': 'Scania S500-770 DC13-16'
        },
    ]

    last_processes_data = [
        {
            'status': 'Done',
            'desc': 'Ford Focus 2011 - DPF off'
        },
        {
            'status': 'Cancelled',
            'desc': 'Fiat Egea 2018 - EGR off'
        },
        {
            'status': 'Done',
            'desc': 'Volkswagen Passat 2019 - Stage-1 Tuning'
        },
        {
            'status': 'Cancelled',
            'desc': 'Ford Focus 2016 - DPF off Stage-2 Tuning'
        },
    ]

    context = {
        'page_title': 'Dashboard',
        'styling_files': ["dashboard.css"],
        'script_files': ["dashboard.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'files_submitted_data': {
            'today': 1,
            'week': 3,
            'month': monthly_file_nums[-1],
            'monthly_data': monthly_data
        },
        'new_know_data': new_know_data,
        'last_processes_data': last_processes_data
    }
    
    return render(request, "pages/dashboard.html", context)

@login_required
def files_page(request):
    context = {
        'page_title': 'Your Files',
        'styling_files': ["files.css"],
        'script_files': ["files.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
    }

    return render(request, "pages/files.html", context)


@login_required
def requested_files_modal(request):
    req_file_list = [
        {
            'num': 1,
            'vehicle': 'Ford Focus 2011',
            'ecu': 'Bosch AJSDO0012',
            'process': 'DPF off Stage-1 Tune',
            'requested_at': '10.11.2022',
            'updated_at': '12.11.2022',
            'status': 'Done'
        },
        {
            'num': 2,
            'vehicle': 'Ford Focus 2012',
            'ecu': 'Bosch AJSDO0013',
            'process': 'DPF off EGR off',
            'requested_at': '10.11.2023',
            'updated_at': '12.11.2023',
            'status': 'Cancelled'
        },
        {
            'num': 3,
            'vehicle': 'Ford Focus 2013',
            'ecu': 'Bosch AJSDO0014',
            'process': 'EGR off Stage-1 Tune',
            'requested_at': '8.11.2022',
            'updated_at': '11.11.2022',
            'status': 'Pending'
        },
        {
            'num': 4,
            'vehicle': 'Ford Focus 2014',
            'ecu': 'Bosch AJSDO2630015',
            'process': 'Stage-1 Tune',
            'requested_at': '9.11.2022',
            'updated_at': '10.11.2022',
            'status': 'Done'
        },
        {
            'num': 5,
            'vehicle': 'Ford Focus 2015',
            'ecu': 'Bosch AJSDO2630016',
            'process': 'DPF off Stage-1 Tune',
            'requested_at': '13.11.2022',
            'updated_at': '15.11.2023',
            'status': 'Cancelled'
        },
        {
            'num': 5,
            'vehicle': 'Ford Focus 2016',
            'ecu': 'Bosch AJSDO2630017',
            'process': 'DPF off',
            'requested_at': '10.11.2022',
            'updated_at': '12.11.2022',
            'status': 'Pending'
        },
        {
            'num': 6,
            'vehicle': 'Ford Focus 2017',
            'ecu': 'Bosch AJSDO2630018',
            'process': 'EGR off',
            'requested_at': '10.11.2022',
            'updated_at': '15.11.2022',
            'status': 'Done'
        },
        {
            'num': 7,
            'vehicle': 'Ford Focus 2018',
            'ecu': 'Bosch AJSDO2630019',
            'process': 'EGR off Stage-1 Tune',
            'requested_at': '10.11.2022',
            'updated_at': '25.11.2022',
            'status': 'Cancelled'
        },
        {
            'num': 8,
            'vehicle': 'Ford Focus 2019',
            'ecu': 'Bosch AJSDO2630020',
            'process': 'DPF off Stage-1 Tune',
            'requested_at': '30.11.2024',
            'updated_at': '12.11.2025',
            'status': 'Pending'
        },
        {
            'num': 9,
            'vehicle': 'Ford Focus 2020',
            'ecu': 'Bosch AJSDO2630021',
            'process': 'DPF off EGR off',
            'requested_at': '10.11.2023',
            'updated_at': '2.11.2027',
            'status': 'Done'
        },
        {
            'num': 10,
            'vehicle': 'Ford Focus 2021',
            'ecu': 'Bosch AJSDO2630022',
            'process': 'DPF off EGR off Stage-1 Tune',
            'requested_at': '10.11.2002',
            'updated_at': '12.11.2012',
            'status': 'Cancelled'
        },
        {
            'num': 11,
            'vehicle': 'Ford Focus 2022',
            'ecu': 'Bosch AJSDO2630023',
            'process': 'DPF off EGR off Stage-1 Tune',
            'requested_at': '10.11.2008',
            'updated_at': '12.11.2022',
            'status': 'Pending'
        },
        {
            'num': 12,
            'vehicle': 'Ford Focus 2023',
            'ecu': 'Bosch AJSDO2630024',
            'process': 'DPF off EGR off Stage-2 Tune',
            'requested_at': '10.11.2009',
            'updated_at': '12.11.2022',
            'status': 'Done'
        },
        {
            'num': 13,
            'vehicle': 'Ford Focus 2024',
            'ecu': 'Bosch AJSDO2630025',
            'process': 'DPF off EGR off Stage-3 Tune',
            'requested_at': '10.11.2022',
            'updated_at': '12.11.2030',
            'status': 'Cancelled'
        },
        {
            'num': 14,
            'vehicle': 'Ford Focus 2022',
            'ecu': 'Bosch AJSDO2630023',
            'process': 'DPF off EGR off Stage-1 Tune',
            'requested_at': '10.11.2008',
            'updated_at': '12.11.2022',
            'status': 'Pending'
        },
        {
            'num': 15,
            'vehicle': 'Ford Focus 2023',
            'ecu': 'Bosch AJSDO2630024',
            'process': 'DPF off EGR off Stage-2 Tune',
            'requested_at': '10.11.2009',
            'updated_at': '12.11.2022',
            'status': 'Done'
        },
        {
            'num': 16,
            'vehicle': 'Ford Focus 2020',
            'ecu': 'Bosch AJSDO2630021',
            'process': 'DPF off EGR off',
            'requested_at': '10.11.2023',
            'updated_at': '2.11.2027',
            'status': 'Done'
        },
        {
            'num': 17,
            'vehicle': 'Ford Focus 2020',
            'ecu': 'Bosch AJSDO2630021',
            'process': 'DPF off EGR off',
            'requested_at': '10.11.2023',
            'updated_at': '2.11.2027',
            'status': 'Done'
        },
        {
            'num': 18,
            'vehicle': 'Ford Focus 2021',
            'ecu': 'Bosch AJSDO2630022',
            'process': 'DPF off EGR off Stage-1 Tune',
            'requested_at': '10.11.2002',
            'updated_at': '12.11.2012',
            'status': 'Cancelled'
        },
        {
            'num': 19,
            'vehicle': 'Ford Focus 2022',
            'ecu': 'Bosch AJSDO2630023',
            'process': 'DPF off EGR off Stage-1 Tune',
            'requested_at': '10.11.2008',
            'updated_at': '12.11.2022',
            'status': 'Pending'
        },
        {
            'num': 20,
            'vehicle': 'Ford Focus 2023',
            'ecu': 'Bosch AJSDO2630024',
            'process': 'DPF off EGR off Stage-2 Tune',
            'requested_at': '10.11.2009',
            'updated_at': '12.11.2022',
            'status': 'Done'
        },
        {
            'num': 21,
            'vehicle': 'Ford Focus 2014',
            'ecu': 'Bosch AJSDO2630015',
            'process': 'Stage-1 Tune',
            'requested_at': '9.11.2022',
            'updated_at': '10.11.2022',
            'status': 'Done'
        },
        {
            'num': 22,
            'vehicle': 'Ford Focus 2015',
            'ecu': 'Bosch AJSDO2630016',
            'process': 'DPF off Stage-1 Tune',
            'requested_at': '13.11.2022',
            'updated_at': '15.11.2023',
            'status': 'Cancelled'
        },
    ]

    params = request.GET
    keyword = params.get('keyword')
    page = params.get('page')

    search_list = []
    if keyword:
        keyword = unquote(keyword).lower()
        for file in req_file_list:
            if keyword in str(file.get('num')).lower() or keyword in file.get('vehicle').lower() or keyword in file.get('ecu').lower() or keyword in file.get('process').lower() or keyword in file.get('requested_at').lower() or keyword in file.get('updated_at').lower() or keyword in file.get('status').lower():
                search_list.append(file)
    else:
        search_list = req_file_list

    data_amount = len(search_list)
    total_pages = math.ceil(len(search_list) / 10)

    if page:
        page = int(page)
        if page > total_pages:
            page = total_pages
        
        if page < 1:
            page = 1
        
    else:
        page = 1
    
    page_list = range(10 * math.floor(page / 10) + 1, min(10 * math.ceil(page / 10), total_pages) + 1)

    start_index = 10 * (page - 1)
    end_index = min(10 * page - 1, data_amount - 1)
    ret_list = search_list[start_index : end_index + 1]

    if page_list:
        any_previous_page = page > page_list[0]
        any_following_page = page < page_list[-1]
    else:
        any_previous_page = False
        any_following_page = False
        page_list = [1]

    context = {
        'data_amount': data_amount,
        'start_index': start_index + 1,
        'end_index': end_index + 1,
        'current_page': page,
        'previous_page_disabled': not any_previous_page,
        'following_page_disabled': not any_following_page,
        'page_list': page_list,
        'requested_file_data': ret_list
    }
    
    return render(request, "modals/requested_files_modal.html", context)

@login_required
def winols_modal(request):
    context = {
        'modal_title': 'Add Your EVC WinOLS Account'
    }

    return render(request, "modals/winols_modal.html", context)

@login_required
def expense_history_page(request):
    context = {
        'page_title': 'Expense History',
        'styling_files': ["expense_history.css"],
        'script_files': ["expense_history.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52
    }

    return render(request, "pages/expense_history.html", context)

@login_required
def expenses_modal(request):
    expenses_data = [
        {
            'amount': '150',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'DPF off, Stage-1 tuning requested for Ford Focus 20118'
        },
        {
            'amount': '50',
            'type': 'Expense',
            'category': 'File purchase',
            'desc': 'Original file of Ford Focus 20147'
        },
        {
            'amount': '100',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'EGR off requested for Ford Focus 20166'
        },
        {
            'amount': '190',
            'type': 'Deposit',
            'category': 'Deposit',
            'desc': 'You have deposited 900 credits'
        },
        {
            'amount': '150',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'DPF off, Stage-1 tuning requested for Ford Focus 20115'
        },
        {
            'amount': '50',
            'type': 'Expense',
            'category': 'File purchase',
            'desc': 'Original file of Ford Focus 20144'
        },
        {
            'amount': '100',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'EGR off requested for Ford Focus 20163'
        },
        {
            'amount': '100',
            'type': 'Deposit',
            'category': 'Deposit',
            'desc': 'You have deposited 100 credits'
        },
        {
            'amount': '120',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'DPF off, Stage-1 tuning requested for Ford Focus 2012'
        },
        {
            'amount': '51',
            'type': 'Expense',
            'category': 'File purchase',
            'desc': 'Original file of Ford Focus 2011'
        },
        {
            'amount': '110',
            'type': 'Expense',
            'category': 'File process',
            'desc': 'EGR off requested for Ford Focus 2011'
        },
        {
            'amount': '1000',
            'type': 'Deposit',
            'category': 'Deposit',
            'desc': 'You have deposited 1000 credits'
        },
    ]

    params = request.GET
    page = params.get('page')

    data_amount = len(expenses_data)
    total_pages = math.ceil(data_amount / 10)

    if page:
        page = int(page)
        if page > total_pages:
            page = total_pages
        
        if page < 1:
            page = 1
        
    else:
        page = 1

    page_list = range(10 * math.floor(page / 10) + 1, min(10 * math.ceil(page / 10), total_pages) + 1)

    start_index = 10 * (page - 1)
    end_index = min(10 * page - 1, data_amount - 1)
    ret_list = expenses_data[start_index : end_index + 1]

    if page_list:
        any_previous_page = page > page_list[0]
        any_following_page = page < page_list[-1]
    else:
        any_previous_page = False
        any_following_page = False
        page_list = [1]

    context = {
        'data_amount': data_amount,
        'start_index': start_index + 1,
        'end_index': end_index + 1,
        'current_page': page,
        'previous_page_disabled': not any_previous_page,
        'following_page_disabled': not any_following_page,
        'page_list': page_list,
        'data': ret_list
    }

    return render(request, "modals/expenses_modal.html", context)

@login_required
def dtc_search_page(request):
    context = {
        'page_title': 'DTC Search',
        'styling_files': ["dtc_search.css"],
        'script_files': ["dtc_search.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52
        }
    
    return render(request, "pages/dtc_search.html", context)

@login_required
def dtc_search_modal(request):
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
        },
        {
            'code': 'P000A',
            'desc': 'No fault 2'
        },
        {
            'code': 'P000B',
            'desc': 'Fuel volume regulator control -circuit open 2'
        },
        {
            'code': 'P000C',
            'desc': 'Fuel volume regulator control -circuit range/performance 2'
        },
        {
            'code': 'P000D',
            'desc': 'Fuel volume regulator control -circuit low 2'
        },
        {
            'code': 'P000E',
            'desc': 'Fuel volume regulator control -circuit high 2'
        },
        {
            'code': 'P000F',
            'desc': 'Fuel shut -off valve -circuit open 2'
        },
        {
            'code': 'P0010',
            'desc': 'Fuel shut -off valve -circuit low 2'
        },
        {
            'code': 'P0011',
            'desc': 'Fuel shut -off valve -circuit high 2'
        },
        {
            'code': 'P0012',
            'desc': 'Engine position system, bank 1 -engine performance 2'
        },
        {
            'code': 'P0013',
            'desc': 'Engine position system, bank 2 -engine performance 2'
        }
    ]

    params = request.GET
    keyword = params.get('keyword')
    page = params.get('page')

    search_list = []
    if keyword:
        keyword = unquote(keyword).lower()
        for dtc in dtc_list:
            if keyword in dtc.get('code').lower() or keyword in dtc.get('desc').lower():
                search_list.append(dtc)
    else:
        search_list = dtc_list

    data_amount = len(search_list)
    total_pages = math.ceil(len(search_list) / 10)

    if page:
        page = int(page)
        if page > total_pages:
            page = total_pages
        
        if page < 1:
            page = 1
        
    else:
        page = 1
    
    page_list = range(10 * math.floor(page / 10) + 1, min(10 * math.ceil(page / 10), total_pages) + 1)

    start_index = 10 * (page - 1)
    end_index = min(10 * page - 1, data_amount - 1)
    ret_list = search_list[start_index : end_index + 1]

    if page_list:
        any_previous_page = page > page_list[0]
        any_following_page = page < page_list[-1]
    else:
        any_previous_page = False
        any_following_page = False
        page_list = [1]

    context = {
        'data_amount': data_amount,
        'start_index': start_index + 1,
        'end_index': end_index + 1,
        'current_page': page,
        'previous_page_disabled': not any_previous_page,
        'following_page_disabled': not any_following_page,
        'page_list': page_list,
        'data': ret_list
    }
    
    return render(request, "modals/dtc_search_modal.html", context)

@login_required
def bosch_search_page(request):
    context = {
        'page_title': 'Bosch Search',
        'styling_files': ["bosch_search.css"],
        'script_files': ["bosch_search.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52
    }

    return render(request, "pages/bosch_search.html", context)

@login_required
def bosch_modal(request):
    ecu_list = [
        {
            'type': 'MED9.5.10',
            'number': '0261S021861',
            'car_manufacturer': 'VW'
        },
        {
            'type': 'MED9.5.10',
            'number': '0261S021372',
            'car_manufacturer': 'AUDI'
        },
        {
            'type': 'MED9.1',
            'number': '0261S021863',
            'car_manufacturer': 'BMW'
        },
        {
            'type': 'MED9.2',
            'number': '0261S021864',
            'car_manufacturer': 'VW'
        },
        {
            'type': 'MED9.3',
            'number': '0261S021865',
            'car_manufacturer': 'AUDI'
        },
        {
            'type': 'MED9.4',
            'number': '0261S021866',
            'car_manufacturer': 'BMW'
        },
        {
            'type': 'MED9.5',
            'number': '0261S021867',
            'car_manufacturer': 'VW'
        },
        {
            'type': 'MED9.6',
            'number': '0261S021868',
            'car_manufacturer': 'AUDI'
        },
        {
            'type': 'MED9.7',
            'number': '0261S021869',
            'car_manufacturer': 'BMW'
        },
        {
            'type': 'MED9.8',
            'number': '0261S0218610',
            'car_manufacturer': 'VW'
        },
        {
            'type': 'MED9.9',
            'number': '0261S0218611',
            'car_manufacturer': 'AUDI'
        },
        {
            'type': 'MED9.10',
            'number': '0261S0218612',
            'car_manufacturer': 'BMW'
        },
        {
            'type': 'MED9.11',
            'number': '0261S0218613',
            'car_manufacturer': 'VW'
        }
    ]

    params = request.GET
    keyword = params.get('keyword')
    page = params.get('page')

    context = {}

    if keyword:
        search_list = []
        keyword = unquote(keyword).lower()
        for ecu in ecu_list:
            if keyword in ecu.get('number').lower():
                search_list.append(ecu)

        data_amount = len(search_list)
        total_pages = math.ceil(len(search_list) / 10)

        if page:
            page = int(page)
            if page > total_pages:
                page = total_pages
            
            if page < 1:
                page = 1
            
        else:
            page = 1
        
        page_list = range(10 * math.floor(page / 10) + 1, min(10 * math.ceil(page / 10), total_pages) + 1)

        start_index = 10 * (page - 1)
        end_index = min(10 * page - 1, data_amount - 1)
        ret_list = search_list[start_index : end_index + 1]

        if page_list:
            any_previous_page = page > page_list[0]
            any_following_page = page < page_list[-1]
        else:
            any_previous_page = False
            any_following_page = False
            page_list = [1]

        context = {
            'results': {
                'data_amount': data_amount,
                'start_index': start_index + 1,
                'end_index': end_index + 1,
                'current_page': page,
                'previous_page_disabled': not any_previous_page,
                'following_page_disabled': not any_following_page,
                'page_list': page_list,
                'search_data': ret_list
            }
        }

    return render(request, "modals/bosch_modal.html", context)

@login_required
def knowledgebase_page(request):
    knowledge_data = [
        {
            'title': 'Adblue Solutions',
            'id': 'adblue_solutions'
        },
        {
            'title': 'MED17 VCDS Logging profiles',
            'id': 'med17_vcds_logging_profiles'
        },
        {
            'title': 'EGR OFF Solutions',
            'id': 'egr_off_solutions'
        }
    ]

    context = {
        'page_title': 'Knowledgebase',
        'styling_files': ["knowledgebase.css"],
        'script_files': ["knowledgebase.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'knowledge_data': knowledge_data
    }
    return render(request, "pages/knowledgebase.html", context)

@login_required
def knowledge_modal(request):
    knowledge_data = {
        'adblue_solutions': {
            'modal_title': 'Adblue Solutions',
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
        'med17_vcds_logging_profiles': {
            'modal_title': 'MED17 VCDS Logging profiles',
            'desc': 'Audi a5 - med171 - gen logs.zip\n\nGeneral logging profiles for the Med17.1 Vag ECU - VCDS Advanced - Open the unzipped file and it will populate the logging profile for you.\nGeneral sweep 1500rpm - redline needed for full scope, highest gear possible for more info'
        },
        'egr_off_solutions': {
            'modal_title': 'EGR OFF Solutions',
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
    }

    params = request.GET
    context = knowledge_data[params.get('id')]

    return render(request, "modals/knowledge_modal.html", context)

@login_required
def pricing_modal(request):

    context = {
        'modal_title': 'File pricing',
        'tax_percentage': '20'
    }
    return render(request, "modals/pricing_modal.html", context)

@login_required
def price_options_modal(request):
    data = {
        'cars': [
            {
                'id': 'stage-one-tune',
                'name': 'Stage one tune',
                'price': '50'
            },
            {
                'id': 'stage-two-tune',
                'name': 'Stage two tune',
                'price': '60'
            }
        ],
        'agricultural': [
            {
                'id': 'gear-box',
                'name': 'Gear box',
                'price': '30'
            }
        ],
        'trucks': [
            {
                'id': 'file-check',
                'name': 'File check',
                'price': '10'
            },
            {
                'id': 'egr-off',
                'name': 'EGR off',
                'price': '30'
            }
        ]
    }

    params = request.GET
    category = params.get('category')
    context = {
        'options': data[category]
    }

    return render(request, "modals/price_options_modal.html", context)



