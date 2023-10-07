from django.contrib import admin
from .models import Customer, Employee, VehicleCategory, VehicleBrand, EngineVersion, VehicleModel, EcuBrand, EcuModel, Ecu, Vehicle, ConnectionTool, FileProcess, ProcessPricing, FileRequest, Knowledge, KnowledgePart, KnowledgeItem, DtcInfo, FileSale, Transaction

# Register your models here.


admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(VehicleCategory)
admin.site.register(VehicleBrand)
admin.site.register(EngineVersion)
admin.site.register(VehicleModel)
admin.site.register(EcuBrand)
admin.site.register(EcuModel)
admin.site.register(Ecu)
admin.site.register(Vehicle)
admin.site.register(ConnectionTool)
admin.site.register(FileProcess)
admin.site.register(ProcessPricing)
admin.site.register(FileRequest)
admin.site.register(Knowledge)
admin.site.register(KnowledgePart)
admin.site.register(KnowledgeItem)
admin.site.register(DtcInfo)
admin.site.register(FileSale)
admin.site.register(Transaction)
