from django.core.serializers import serialize
from django.shortcuts import render
from database.models import *
from django.http import JsonResponse
from urllib.parse import unquote
from django.core.paginator import Paginator
from django.db.models import Q

from functools import reduce
import operator
import json

from database.models import *

# Create your views here.

def get_vehicle_queries(filters):
    vehicle_filters = json.loads(filters)
    q_list = []
    for key, value in vehicle_filters.items():
        if key == 'vehicle_years':
            q_list.append(Q(vehicle_year_id__in=value))
        
        elif key == 'vehicle_versions':
            q_list.append(Q(version_id__in=value))

        elif key == 'ecu_models':
            q_list.append(Q(ecu_model_id__in=value))

    return q_list

def vehicle_data_api(request):
    params = request.GET

    requests = json.loads(params.get('requests'))

    data = {}
    for requested in requests:
        if requested == 'vehicle_category':
            vehicle_categories = VehicleCategory.objects.all().order_by('name')
            data["vehicle_category"] = serialize("json", vehicle_categories, fields=['id', 'name'])
        
        elif requested == 'vehicle_brand':
            category_ids = json.loads(params.get('vehicle_categories'))
            vehicle_model_ids = VehicleModel.objects.filter(category_id__in=category_ids).values('brand_id')
            vehicle_brands = VehicleBrand.objects.filter(id__in=vehicle_model_ids).order_by('name')
            data["vehicle_brand"] = serialize("json", vehicle_brands, fields=['id', 'name'])

        elif requested == 'vehicle_model':
            category_ids = json.loads(params.get('vehicle_categories'))
            brand_ids = json.loads(params.get('vehicle_brands'))
            vehicle_models = VehicleModel.objects.filter(category_id__in=category_ids, brand_id__in=brand_ids).order_by('brand__name','category__name','name')
            
            models_data = []
            for model in vehicle_models:
                models_data.append({
                    'id': model.id,
                    'name': model.name,
                    'category_id': model.category.id,
                    'brand_id': model.brand.id,
                    'brand_name': model.brand.name,
                    'category_name': model.category.name
                })

            data["vehicle_model"] = models_data
        
        elif requested == 'vehicle_year':
            model_ids = json.loads(params.get('vehicle_models'))
            years = VehicleYear.objects.filter(model_id__in=model_ids).order_by('model__name', 'year')

            years_data = []
            for year in years:
                years_data.append({
                    'id': year.id,
                    'year': year.year,
                    'model_id': year.model.id,
                    'brand_model_name': str(year.model),
                })

            data["vehicle_year"] = years_data

        elif requested == 'vehicle_version':
            vehicle_year_ids = json.loads(params.get('vehicle_years'))
            vehicle_version_ids = Vehicle.objects.filter(vehicle_year_id__in=vehicle_year_ids).values('version_id')
            engines = VehicleVersion.objects.filter(id__in=vehicle_version_ids).order_by('name', 'fuel_type')
            data["vehicle_version"] = serialize("json", engines, fields=['id', 'name', 'fuel_type'])

        elif requested == 'ecu_type':
            vehicle_year_ids = json.loads(params.get('vehicle_years'))
            version_ids = json.loads(params.get('vehicle_versions'))
            ecu_model_ids = Vehicle.objects.filter(vehicle_year_id__in=vehicle_year_ids, version_id__in=version_ids).values('ecu_model_id')
            ecu_models = EcuModel.objects.filter(id__in=ecu_model_ids).order_by('brand__name', 'name')

            ecu_data = []
            for ecu in ecu_models:
                ecu_data.append({
                    'id': ecu.id,
                    'name': ecu.name,
                    'brand_id': ecu.brand.id,
                    'brand_name': ecu.brand.name
                })

            data["ecu_type"] = ecu_data

        elif requested == 'vehicle':
            vehicle_filters = params.get('vehicle_filters')
            queries = get_vehicle_queries(vehicle_filters)
            vehicles = Vehicle.objects.filter(reduce(operator.and_, queries))

            page = params.get('vehicle_page')
            if page is not None:
                pagenum = int(page)

                paginator = Paginator(vehicles, 10)
                page = paginator.page(int(pagenum))
                start_page = max(1, page.number - 5)
                end_page = min(paginator.num_pages, max(page.number + 5, 10))
                page_list = list(range(start_page, end_page + 1))

                vehicle_data = []
                for vehicle in page.object_list:
                    vehicle_data.append({
                        'id': vehicle.id,
                        'vehicle_category': vehicle.vehicle_year.model.category.name,
                        'vehicle_brand': vehicle.vehicle_year.model.brand.name,
                        'vehicle_model': vehicle.vehicle_year.model.name,
                        'vehicle_year': vehicle.vehicle_year.year,
                        'vehicle_version': vehicle.version.name,
                        'ecu_model': vehicle.ecu_model.name
                    })

                data["vehicle"] = {
                    'data_amount': paginator.count,
                    'start_index': page.start_index(),
                    'end_index': page.end_index(),
                    'current_page': page.number,
                    'previous_page_disabled': not page.has_previous(),
                    'following_page_disabled': not page.has_next(),
                    'page_list': page_list,
                    'data': vehicle_data
                }
            else:
                vehicle_data = []
                for vehicle in vehicles:
                    vehicle_data.append({
                        'id': vehicle.id,
                        'vehicle_category': vehicle.vehicle_year.model.category.name,
                        'vehicle_brand': vehicle.vehicle_year.model.brand.name,
                        'vehicle_model': vehicle.vehicle_year.model.name,
                        'vehicle_year': vehicle.vehicle_year.year,
                        'vehicle_version': vehicle.version.name,
                        'ecu_model': vehicle.ecu_model.name
                    })
                data["vehicle"] = {
                    'data_amount': vehicles.count(),
                    'data': vehicle_data
                }

    context = {
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
