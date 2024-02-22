from django.db import models

# Create your models here.
class VehicleCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class VehicleBrand(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name
    
class VehicleModel(models.Model):
    name = models.CharField(max_length=40)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    category = models.ForeignKey(VehicleCategory, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['brand', 'name', 'category'], name='vehiclemodel_brand_name_category_unique_constraint')
        ]

    def __str__(self):
        return str(self.brand) + " " + self.name
    
class VehicleYear(models.Model):
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'year'], name='vehicleyear_model_year_constraint')
        ]

    def __str__(self):
        return str(self.model) + " " + str(self.year)
    
class VehicleVersion(models.Model):
    fuel_type_choices = [
        ("P", "Petrol"),
        ("D", "Diesel"),
        ("EL", "Electric"),
        ("L", "LPG"),
        ("E", "Ethanol"),
        ("C", "CNG"),
        ("PL", "Petrol/LPG"),
        ("PE", "Petrol/Ethanol"),
        ("PC", "Petrol/CNG"),
        ("H", "Hybrid"),
    ]
    
    name = models.CharField(max_length=60)
    fuel_type = models.CharField(max_length=2, choices=fuel_type_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'fuel_type'], name='vehicleversion_name_fueltype_unique_constraint')
        ]

    def __str__(self):
        for ftc in self.fuel_type_choices:
            if ftc[0] == self.fuel_type:
                fuel_type = ftc[1]

        return self.name + " - " + fuel_type
    
class EcuBrand(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class EcuModel(models.Model):
    name = models.CharField(max_length=30)
    brand = models.ForeignKey(EcuBrand, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='ecumodel_name_brand_unique_constraint')
        ]

    def __str__(self):
        return str(self.brand) + " " + self.name
    
class Vehicle(models.Model):
    vehicle_year = models.ForeignKey(VehicleYear, on_delete=models.CASCADE)
    version = models.ForeignKey(VehicleVersion, on_delete=models.PROTECT)
    ecu_model = models.ForeignKey(EcuModel, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle_year', 'version', 'ecu_model'], name='vehicle_vehicleyear_version_ecumodel_unique_constraint')
        ]
    
    @classmethod
    def get_version_option_list(cls, **kwargs):
        ret_list = []
        for instance in cls.objects.filter(kwargs):
            if instance.version not in ret_list:
                ret_list.append(instance.version)

        return ret_list
    
    @classmethod
    def get_ecu_model_option_list(cls, **kwargs):
        ret_list = []
        for instance in cls.objects.filter(kwargs):
            if instance.version not in ret_list:
                ret_list.append(instance.ecu_model)
                
        return ret_list
    
    def __str__(self):
        return str(self.vehicle_year) + " - " + str(self.version) + " - " + str(self.ecu_model)  

class ConnectionTool(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name
    
class VehiclePotential(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    old_hp = models.PositiveIntegerField()
    new_hp = models.PositiveIntegerField()
    old_nm = models.PositiveIntegerField()
    new_nm = models.PositiveIntegerField()
    known_reading_methods = models.ManyToManyField(ConnectionTool)

class Ecu(models.Model):
    model = models.ForeignKey(EcuModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    carmanufacturers = models.CharField(max_length=130, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'number'], name='ecu_model_number_unique_constraint')
        ]
    
    def __str__(self):
        return self.number

class DtcInfo(models.Model):
    code = models.CharField(max_length=7)
    desc = models.TextField(max_length=1000)

    def __str__(self):
        return self.code + " dtc"
