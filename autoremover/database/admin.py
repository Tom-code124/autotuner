from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(VehicleCategory)
admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)
admin.site.register(VehicleYear)
admin.site.register(VehicleVersion)
admin.site.register(Vehicle)
admin.site.register(EcuBrand)
admin.site.register(EcuModel)
admin.site.register(Ecu)
admin.site.register(ConnectionTool)
admin.site.register(VehiclePotential) # custom page needed
admin.site.register(FileProcess)
admin.site.register(ProcessPricing) # custom page needed
admin.site.register(FileRequest) # custom page needed for employee side , or readonly fields can solve the issue
admin.site.register(FileSale)
admin.site.register(Transaction) # custom page needed (only deposit)
admin.site.register(Knowledge)
admin.site.register(KnowledgePart)
admin.site.register(KnowledgeBullet)
admin.site.register(KnowledgeAd)
admin.site.register(DtcInfo)
admin.site.register(FileService) # custom page needed (only employee)
admin.site.register(FileServiceSchedule) # custom page needed (only employee)
admin.site.register(SystemSetting)
