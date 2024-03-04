from django.core.serializers import serialize
from django.shortcuts import render
from database.models import *
from django.http import JsonResponse
import json

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

    context = {
        'data_type': data_type,
        'data': data
    }

    return JsonResponse(context)
