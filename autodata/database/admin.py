from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from .models import *

# Register your models here.

admin.site.register(VehicleCategory)
admin.site.register(VehicleBrand)

class VehicleYearInline(admin.TabularInline):
    model = VehicleYear
    extra = 1

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    inlines = [VehicleYearInline]
    search_fields = ("brand__name", "name", )
    list_per_page = 20

@admin.register(VehicleYear)
class VehicleYearAdmin(admin.ModelAdmin):
    autocomplete_fields = ("model", )
    search_fields = ("model__name", "model__brand__name")
    list_per_page = 10

@admin.register(VehicleVersion)
class VehicleVersionAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_per_page = 10

class EcuModelFilter(AutocompleteFilter):
    title = 'Ecu Model'
    field_name = 'ecu_model'

class VehicleYearFilter(AutocompleteFilter):
    title = 'Vehicle Year'
    field_name = 'vehicle_year'

class PotentialInline(admin.TabularInline):
    model = VehiclePotential
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [PotentialInline]
    fields = ("vehicle_year", "version", "ecu_model")
    search_fields = ["vehicle_year__model__name", "vehicle_year__model__brand__name", "version__name", "ecu_model__name"]
    autocomplete_fields = ("vehicle_year", "version", "ecu_model")
    actions = ['make_pricing']
    list_display = ("vehicle_year", "version", "ecu_model")
    list_per_page = 10
    
    # @admin.action
    # def make_pricing(self, request, queryset):
    #     if 'apply' in request.POST:
    #         vehicle_ids = request.POST.getlist("_selected_action")
    #         master_price = float(request.POST.get("master_price"))
    #         slave_price = float(request.POST.get("slave_price"))
    #         euro_price = float(request.POST.get("euro_price"))
    #         process_id = int(request.POST.get("process"))

    #         for vehicle_id in vehicle_ids:
    #             pricing, created = ProcessPricing.objects.get_or_create(vehicle_id=int(vehicle_id), process_id=process_id, defaults={
    #                 "master_price": master_price,
    #                 "slave_price": slave_price,
    #                 "euro_price": euro_price
    #                 })

    #             if not created:
    #                 pricing.master_price = master_price
    #                 pricing.slave_price = slave_price
    #                 pricing.euro_price = euro_price
    #                 pricing.save()
            
    #         self.message_user(request, "Pricing is done as " + str(master_price) + ", " + str(slave_price) + ", " + str(euro_price) + " with process id: " + str(process_id) + " on " + str(len(vehicle_ids)) + " vehicles!")
    #         return HttpResponseRedirect(request.get_full_path())

    #     processes = FileProcess.objects.all()
    #     context = {
    #         'vehicles': queryset,
    #         'processes': processes
    #     }
    #     return render(request, 'admin/make_pricing.html', context)
    
    def get_actions(self, request):
        actions = super(VehicleAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['make_pricing']
        return actions
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return [EcuModelFilter, VehicleYearFilter]
        return []

admin.site.register(EcuBrand)
@admin.register(EcuModel)
class EcuModelAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_filter = ("brand", )
    list_display = ("name", "brand")
    list_per_page = 20

admin.site.register(Ecu)
admin.site.register(ConnectionTool)

@admin.register(DtcInfo)
class DtcInfoAdmin(admin.ModelAdmin):
    search_fields = ['code', 'desc']
    list_display = ['code', 'desc']
