from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from database.models import *
from database.forms import *

from datetime import datetime
from urllib.parse import unquote
import math

# Create your views here.

def signup_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/app/')

    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST or None)
        customer_form = CustomerCreationForm(request.POST or None)

        if all((user_form.is_valid(), customer_form.is_valid())):
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/app/')
        
    else:
        user_form = ExtendedUserCreationForm()
        customer_form = CustomerCreationForm()

    context = {
        'page_title': 'Sign-up',
        'styling_files': ["customer_signup.css"],
        'customer_form': customer_form,
        'user_form': user_form
    }

    return render(request, "pages/customer_signup.html", context)

def login_page(request):
    user = request.user
    if user.is_authenticated:
        try:
            if user.customer is not None:
                return redirect('/app/')
        except:
            messages.error(request, "You are not authorazied to do this!")
            logout(request)
            return redirect('/app/login/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                if user.customer is not None:
                    login(request, user)
                    redirect_url = request.POST.get('next') if request.POST.get('next') else "/app/"
                    return redirect(redirect_url)
            except:
                messages.error(request, "You are not authorazied to do this!")

        else:
            messages.error(request, "Invalid username or password")

    context = {
        'page_title': 'Log-in',
        'styling_files': ["customer_login.css"],
        'script_files': ["customer_login.js"],
        }

    return render(request, "pages/customer_login.html", context)

def logout_view(request):
    logout(request)
    return redirect('/app/login/')
    
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
    params = request.GET
    subpage = params.get("subpage")

    boughts_open = False

    if subpage == "bought_files":
        boughts_open = True

    context = {
        'page_title': 'Your Files',
        'styling_files': ["files.css"],
        'script_files': ["files.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'boughts_open': boughts_open
    }

    return render(request, "pages/files.html", context)


@login_required
def requested_files_modal(request):
    params = request.GET
    keyword = params.get('keyword')
    page_param = params.get('page')

    req_file_list = FileRequest.objects.filter(customer=request.user.customer).order_by("-updated_at")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(req_file_list, 10)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)

    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'requested_file_data': page.object_list
    }
    
    return render(request, "modals/requested_files_modal.html", context)

@login_required
def bought_files_modal(request):
    params = request.GET
    keyword = params.get('keyword')
    page_param = params.get('page')

    if keyword:
        keyword = unquote(keyword)
        key_file_list = FileSale.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        bought_file_list = FilePurchase.objects.filter(Q(customer_id=request.user.customer.id) | Q(file_sale__in=key_file_list)).order_by("-bought_at")
    else:
        bought_file_list = FilePurchase.objects.filter(customer=request.user.customer).order_by("-bought_at")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(bought_file_list, 10)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)

    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'data': bought_file_list
    }

    return render(request, "modals/bought_files_modal.html", context)

@login_required
def upload_page(request):
    vehicle_categories = VehicleCategory.objects.all()
    connection_tools = ConnectionTool.objects.all()

    if request.method == "POST":
        process_selection = request.POST.getlist("process_selection")
        vehicle_id = int(request.POST.get("vehicle"))

        total_price = 0
        for p in process_selection:
            pricing = ProcessPricing.objects.get(vehicle_id=vehicle_id, process_id=int(p))
            total_price += pricing.price
        
        if request.user.customer.credit_amount >= total_price:
            original_file = request.FILES.get("original_file")
            file_type = request.POST.get("file_type")
            vehicle_engine_id = int(request.POST.get("vehicle_engine"))
            ecu_model_id = request.POST.get("ecu_type")
            manual_ecu_type = request.POST.get("manual_ecu_type")
            transmission_type = request.POST.get("transmission_type")
            tool_id = int(request.POST.get("tool"))
            tool_type = request.POST.get("tool_type")
            customer_description = request.POST.get("customer_description")

            file_request = FileRequest.objects.create(
                customer=request.user.customer,
                vehicle_id=vehicle_id,
                engine_id=vehicle_engine_id,
                file_type=file_type,
                transmission=transmission_type,
                tool_id=tool_id,
                tool_type=tool_type,
                customer_description=customer_description,
                original_file=original_file
                )
            
            if ecu_model_id == "null":
                file_request.manual_provided_ecu = manual_ecu_type
            else:
                file_request.ecu_model = EcuModel.objects.get(id=int(ecu_model_id))

            file_request.save()

            for p in process_selection:
                file_request.processes.add(int(p))
                
            transaction = Transaction.objects.create(customer=request.user.customer, type="E", file_request=file_request, amount=file_request.total_price)
            transaction.save()

            messages.success(request, "File successfully requested!")
            return redirect("/app/files")
        
        else:
            messages.error(request, "You don't have enough credits to request these processes. Please buy some credits.")

    context = {
        'page_title': 'Upload',
        'styling_files': ["upload.css"],
        'script_files': ["upload.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'vehicle_category_list': vehicle_categories,
        'connection_tool_list': connection_tools,
        'tax_percentage': 20
    }

    return render(request, "pages/upload.html", context)

@login_required
def vehicle_select_modal(request):
    params = request.GET

    requested = params.get('requested')
     
    if requested == 'vehicle-brand-select-2':
        category_id = params.get('vehicle-category-select-1')
        category = VehicleCategory.objects.get(id=category_id) 
        vehicle_model_ids = VehicleModel.objects.filter(category=category).values('brand_id')
        vehicle_brands = VehicleBrand.objects.filter(id__in=vehicle_model_ids)
        data_type = 'vehicle brand'
        data = vehicle_brands

    elif requested == 'vehicle-model-select-3':
        category_id = params.get('vehicle-category-select-1')
        brand_id = params.get('vehicle-brand-select-2')
        category = VehicleCategory.objects.get(id=category_id)
        brand = VehicleBrand.objects.get(id=brand_id)
        vehicle_models = VehicleModel.objects.filter(category=category, brand=brand)
        data_type = 'vehicle model'
        data = vehicle_models
    
    elif requested == 'vehicle-year-select-4':
        model_id = params.get('vehicle-model-select-3')
        model = VehicleModel.objects.get(id=model_id)
        years = Vehicle.objects.filter(model=model)
        data_type = 'vehicle year'
        data = years

    elif requested == 'vehicle-engine-select-5':
        vehicle_id = params.get('vehicle-year-select-4')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        engines = VehicleEngine.objects.filter(vehicle=vehicle)
        data_type = 'vehicle engine'
        data = engines

    elif requested == 'ecu-type-select-6':
        vehicle_id = params.get('vehicle-year-select-4')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        ecu_models = EcuModel.objects.filter(vehicles__id=vehicle_id)
        data_type = 'ecu type'
        data = ecu_models

    context = {
        'data_type': data_type,
        'data': data
    }

    return render(request, "modals/upload_selects_modal.html", context)

@login_required
def process_options_modal(request):
    params = request.GET

    vehicle_id = params.get("vehicle_id")
    pricing_options = ProcessPricing.objects.filter(vehicle_id=vehicle_id)

    context = {
        'options': pricing_options
    }

    return render(request, "modals/price_options_modal.html", context)

@login_required
def shop_page(request):

    context = {
        'page_title': 'File Shop',
        'styling_files': ["shop.css"],
        'script_files': ["shop.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
    }

    return render(request, "pages/shop.html", context)

@login_required
def shop_modal(request):

    params = request.GET
    keyword = params.get('keyword')
    page_param = params.get('page')

    if keyword:
        keyword = unquote(keyword).lower()
        file_list = FileSale.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword)).order_by("-created_at")
    else:
        file_list = FileSale.objects.all().order_by("-created_at")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(file_list, 20)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)
    data = []

    for p in page.object_list:
        ownership_bool = FilePurchase.objects.filter(customer=request.user.customer, file_sale=p).count() > 0
        hash = {
            'file': p,
            'ownership_bool': ownership_bool
        }

        data.append(hash)
        
    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'data': data
    }

    return render(request, "modals/shop_modal.html", context)

@login_required
def product_modal(request):
    params = request.GET
    file_id = int(params.get("id"))

    file = FileSale.objects.get(id=file_id)

    context = {
        'modal_title': file.title,
        'file': file
    }

    return render(request, "modals/product_modal.html", context)

@login_required
def purchase_file(request):

    params = request.POST
    file_id = int(params.get("file_id"))
    file = FileSale.objects.get(id=file_id)

    if request.user.customer.credit_amount >= file.price:
        file_purchase = FilePurchase.objects.create(file_sale=file, customer=request.user.customer)
        file_purchase.save()

        transaction = Transaction.objects.create(customer=request.user.customer, type="E", file_bought=file_purchase.file_sale, amount=file_purchase.file_sale.price)
        transaction.save()

        messages.success(request, "File bought successfully!")
        return redirect('/app/files?subpage=bought_files')
    else:
        messages.error(request, "You don't have enough credits to buy this file. Please buy some credits.")
        return redirect("/app/shop/")


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
    }

    return render(request, "pages/expense_history.html", context)

@login_required
def expenses_modal(request):

    params = request.GET
    page_param = params.get('page')

    expenses_data = Transaction.objects.filter(customer=request.user.customer).order_by("-updated_at")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(expenses_data, 10)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)
        
    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'data': page.object_list
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

    params = request.GET
    keyword = params.get('keyword')
    page_param = params.get('page')

    if keyword:
        keyword = unquote(keyword).lower()
        dtc_list = DtcInfo.objects.filter(Q(desc__icontains=keyword) | Q(code__icontains=keyword)).order_by("code")
    else:
        dtc_list = DtcInfo.objects.all().order_by("code")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(dtc_list, 10)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)
        
    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'data': page.object_list
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

    context = {
        'page_title': 'Knowledgebase',
        'styling_files': ["knowledgebase.css"],
        'script_files': ["knowledgebase.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'username': 'yunus',
        'user_credit_amount': 13.52,
        'knowledge_data': Knowledge.objects.all()
    }

    return render(request, "pages/knowledgebase.html", context)

@login_required
def knowledge_modal(request):
    params = request.GET
    knowledge = Knowledge.objects.get(id=params.get('id'))
    inner_data = []
    print(knowledge.knowledgepart_set.all())
    for p in knowledge.knowledgepart_set.all():
        bullets = []
        for b in p.knowledgebullet_set.all():
            bullets.append(b.content)

        part = {
            'sub_title': p.title,
            'bullets': bullets
        }

        inner_data.append(part)

    context = {
        'modal_title': knowledge.title,
        'desc': knowledge.desc,
        'link_title': knowledge.link_title,
        'link': knowledge.link,
        'inner_data': inner_data
    }

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
                'process': 'Stage one tune',
                'price': '50'
            },
            {
                'id': 'stage-two-tune',
                'process': 'Stage two tune',
                'price': '60'
            }
        ],
        'agricultural': [
            {
                'id': 'gear-box',
                'process': 'Gear box',
                'price': '30'
            }
        ],
        'trucks': [
            {
                'id': 'file-check',
                'process': 'File check',
                'price': '10'
            },
            {
                'id': 'egr-off',
                'process': 'EGR off',
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



