from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from database.models import *
from database.forms import *

from django.utils import timezone

from datetime import datetime
from urllib.parse import unquote

# Create your views here.

def signup_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/app/')

    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST or None)
        customer_form = CustomerCreationForm(request.POST or None)

        if all((user_form.is_valid(), customer_form.is_valid())):
            print("forms are valid")
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password1']

            user = authenticate(username=email, password=password)

            if user is not None:
                print("user is not none")
                login(request, user)
                return redirect('/app/')
            
        else:
            messages.error(request, "This email or phone number has already taken by another user!")
        
    else:
        user_form = ExtendedUserCreationForm()
        customer_form = CustomerCreationForm()

    context = {
        'page_title': 'Sign-up',
        'styling_files': [],
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
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
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
        'styling_files': [],
        'script_files': [],
        }

    return render(request, "pages/customer_login.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/app/login/')

@login_required
def deposit_modal(request):
    system_setting = SystemSetting.objects.all()[0]

    context = {
        'modal_title': "Deposit Credits",
        'bank_name': system_setting.bank_name,
        'swift_num': system_setting.swift_number,
        'iban_num': system_setting.iban_number,
        'account_owner': system_setting.bank_account_owner_name,
        'try_price': system_setting.credit_try_price,
        'eur_price': system_setting.credit_eur_price
    }

    return render(request, "modals/deposit_modal.html", context)
    
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
        'styling_files': [],
        'script_files': ["dashboard.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': timezone.now(),
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

    tax_percentage = SystemSetting.objects.all()[0].tax_percentage

    if request.method == "POST":
        process_selection = request.POST.getlist("process_selection")
        vehicle_year_id = int(request.POST.get("vehicle_year"))
        version_id = int(request.POST.get("vehicle_version"))
        ecu_model_id = int(request.POST.get("ecu_type"))
        vehicle = Vehicle.objects.get(vehicle_year_id=vehicle_year_id, version_id=version_id, ecu_model_id=ecu_model_id)

        pricing_class = request.user.customer.pricing_class

        total_price = 0
        for p in process_selection:
            pricing = ProcessPricing.objects.get(vehicle=vehicle, process_id=int(p))
            
            if pricing_class == "M":
                total_price += pricing.master_price
            elif pricing_class == "S":
                total_price += pricing.slave_price
            elif pricing_class == "E":
                total_price += pricing.euro_price
        
        total_price *= 1 + (tax_percentage / 100)
        
        if request.user.customer.credit_amount >= total_price:
            original_file = request.FILES.get("original_file")
            file_type = request.POST.get("file_type")
            transmission_type = request.POST.get("transmission_type")
            tool_id = int(request.POST.get("tool"))
            tool_type = request.user.customer.pricing_class
            customer_description = request.POST.get("customer_description")

            file_request = FileRequest.objects.create(
                customer=request.user.customer,
                vehicle=vehicle,
                file_type=file_type,
                transmission=transmission_type,
                tool_id=tool_id,
                tool_type=tool_type,
                customer_description=customer_description,
                original_file=original_file
                )

            file_request.save()

            for p in process_selection:
                file_request.processes.add(int(p))

            messages.success(request, "File successfully requested!")
            return redirect("/app/files")
        
        else:
            messages.error(request, "You don't have enough credits to request these processes. You can see the depositing details by clicking the wallet sign at the top right corner of the page.")

    context = {
        'page_title': 'Upload',
        'styling_files': ["upload.css"],
        'script_files': ["upload.js"],
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'vehicle_category_list': vehicle_categories,
        'connection_tool_list': connection_tools,
        'tax_percentage': tax_percentage
    }

    return render(request, "pages/upload.html", context)

@login_required
def vehicle_select_modal(request):
    params = request.GET

    requested = params.get('requested')
     
    if requested == 'vehicle_brand':
        category_id = int(params.get('vehicle_category'))
        vehicle_model_ids = VehicleModel.objects.filter(category_id=category_id).values('brand_id')
        vehicle_brands = VehicleBrand.objects.filter(id__in=vehicle_model_ids)
        data_type = 'vehicle brand'
        data = vehicle_brands

    elif requested == 'vehicle_model':
        category_id = int(params.get('vehicle_category'))
        brand_id = int(params.get('vehicle_brand'))
        vehicle_models = VehicleModel.objects.filter(category_id=category_id, brand_id=brand_id)
        data_type = 'vehicle model'
        data = vehicle_models
    
    elif requested == 'vehicle_year':
        model_id = int(params.get('vehicle_model'))
        years = VehicleYear.objects.filter(model_id=model_id)
        data_type = 'vehicle year'
        data = years

    elif requested == 'vehicle_version':
        vehicle_year_id = int(params.get('vehicle_year'))
        vehicle_version_ids = Vehicle.objects.filter(vehicle_year_id=vehicle_year_id).values('version_id')
        engines = VehicleVersion.objects.filter(id__in=vehicle_version_ids)
        data_type = 'vehicle version'
        data = engines

    elif requested == 'ecu_type':
        vehicle_year_id = int(params.get('vehicle_year'))
        version_id = int(params.get('vehicle_version'))
        ecu_model_ids = Vehicle.objects.filter(vehicle_year_id=vehicle_year_id, version_id=version_id).values('ecu_model_id')
        ecu_models = EcuModel.objects.filter(id__in=ecu_model_ids)
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

    vehicle_year_id = int(params.get("vehicle_year_id"))
    version_id = int(params.get("vehicle_version_id"))
    ecu_model_id = int(params.get("ecu_model_id"))

    vehicle = Vehicle.objects.get(vehicle_year_id=vehicle_year_id, version_id=version_id, ecu_model_id=ecu_model_id)
    
    pricing_options = ProcessPricing.objects.filter(vehicle=vehicle)

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
        messages.error(request, "You don't have enough credits to buy this file. You can see the depositing details by clicking the wallet sign at the top right corner of the page.")
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
        'styling_files': [],
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
    }

    return render(request, "pages/bosch_search.html", context)

@login_required
def bosch_modal(request):

    params = request.GET
    keyword = params.get('keyword')
    page_param = params.get('page')

    if keyword:
        keyword = unquote(keyword).lower()
        ecu_list = Ecu.objects.filter(Q(number__icontains=keyword)).order_by("id")

        if page_param:
            pagenum = int(page_param)
        else:
            pagenum = 1

        paginator = Paginator(ecu_list, 10)
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
    
    else:
        context = {}

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

@login_required
def download_file(request):
    customer = request.user.customer
    params = request.GET

    file_type = params.get("file_type")
    model_id = int(params.get("id"))

    if file_type is not None:
        if file_type == "request":
            l = customer.filerequest_set.filter(id=model_id)
            if l.count() > 0:
                file_request = l[0]
                which = params.get("which")
                if which == "original":
                    return FileResponse(file_request.original_file, as_attachment=True)
                elif which == "processed":
                    return FileResponse(file_request.processed_file, as_attachment=True)

        elif file_type == "sale":
            l = customer.filepurchase_set.filter(file_sale_id=model_id)
            if l.count() > 0:
                file_sale = l[0].file_sale
                return FileResponse(file_sale.file)

