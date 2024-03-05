from django.core.serializers import serialize
from django.shortcuts import render
from database.models import *
from django.http import JsonResponse
from urllib.parse import unquote
from django.core.paginator import Paginator
from django.db.models import Q

import json

from database.models import *

# Create your views here.

def vehicle_select_api(request):
    params = request.GET

    requested = params.get('requested')

    if requested == 'vehicle_category':
        vehicle_categories = VehicleCategory.objects.all().order_by('name')
        data_type = 'vehicle category'
        data = serialize("json", vehicle_categories, fields=['id', 'name'])
     
    elif requested == 'vehicle_brand':
        category_id = int(params.get('vehicle_category'))
        vehicle_model_ids = VehicleModel.objects.filter(category_id=category_id).values('brand_id')
        vehicle_brands = VehicleBrand.objects.filter(id__in=vehicle_model_ids).order_by('name')
        data_type = 'vehicle brand'
        data = serialize("json", vehicle_brands, fields=['id', 'name'])

    elif requested == 'vehicle_model':
        category_id = int(params.get('vehicle_category'))
        brand_id = int(params.get('vehicle_brand'))
        vehicle_models = VehicleModel.objects.filter(category_id=category_id, brand_id=brand_id).order_by('name')
        data_type = 'vehicle model'
        data = serialize("json", vehicle_models, fields=['id', 'name'])
    
    elif requested == 'vehicle_year':
        model_id = int(params.get('vehicle_model'))
        years = VehicleYear.objects.filter(model_id=model_id).order_by('year')
        data_type = 'vehicle year'
        data = serialize("json", years, fields=['id', 'year'])

    elif requested == 'vehicle_version':
        vehicle_year_id = int(params.get('vehicle_year'))
        vehicle_version_ids = Vehicle.objects.filter(vehicle_year_id=vehicle_year_id).values('version_id')
        engines = VehicleVersion.objects.filter(id__in=vehicle_version_ids).order_by('name', 'fuel_type')
        data_type = 'vehicle version'
        data = serialize("json", engines, fields=['id', 'name', 'fuel_type'])

    elif requested == 'ecu_type':
        vehicle_year_id = int(params.get('vehicle_year'))
        version_id = int(params.get('vehicle_version'))
        ecu_model_ids = Vehicle.objects.filter(vehicle_year_id=vehicle_year_id, version_id=version_id).values('ecu_model_id')
        ecu_models = EcuModel.objects.filter(id__in=ecu_model_ids).order_by('brand__name', 'name')
        data_type = 'ecu type'
        data = serialize("json", ecu_models, fields=['id', 'name'])

    elif requested == 'vehicle':
        vehicle_year_id = int(params.get("vehicle_year_id"))
        version_id = int(params.get("vehicle_version_id"))
        ecu_model_id = int(params.get("ecu_model_id"))

        vehicle = Vehicle.objects.get(vehicle_year_id=vehicle_year_id, version_id=version_id, ecu_model_id=ecu_model_id)
        data_type = 'vehicle'
        data = {'id': vehicle.id}

    context = {
        'data_type': data_type,
        'data': data
    }

    return JsonResponse(context)

def dtc_search_api(request):
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
    page_list = list(range(start_page, end_page + 1))
        
    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'data': serialize("json", page.object_list, fields=['code', 'desc'])
    }

    return JsonResponse(context)

def bosch_search_api(request):
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
        page_list = list(range(start_page, end_page + 1))
        data = []
        for ecu in page.object_list:
            data.append({
                'number': ecu.number,
                'type': ecu.model.name,
                'carmanufacturers': ecu.carmanufacturers
            })
   
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
    
    else:
        context = {}

    return JsonResponse(context)
