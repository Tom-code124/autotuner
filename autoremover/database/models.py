from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Customer(models.Model):
    phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+905551234567'. Up to 15 digits allowed.")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=16, unique=True)
    credit_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
class VehicleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class VehicleBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class VehicleModel(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(VehicleCategory, on_delete=models.PROTECT)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['brand', 'name'], name='vehiclemodel_brand_name_unique_constraint')
        ]

    def __str__(self):
        return str(self.brand) + " " + self.name

class Vehicle(models.Model):
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'year'], name='vehicle_model_year_constraint')
        ]

    def __str__(self):
        return str(self.model) + " " + str(self.year)

class VehicleEngine(models.Model):
    fuel_type_choices = [
        ("P", "Petrol"),
        ("D", "Diesel")
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hp = models.IntegerField()
    fuel_type = models.CharField(max_length=1, choices=fuel_type_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'name', 'hp'], name='vehicleengine_vehicle_name_hp_unique_constraint')
        ]

    def __str__(self):
        return self.name + " - " + self.fuel_type + " - " + str(self.hp)

class EcuBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class EcuModel(models.Model): # for ecu type
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(EcuBrand, on_delete=models.CASCADE)
    vehicles = models.ManyToManyField(Vehicle, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='ecumodel_name_brand_unique_constraint')
        ]

    def __str__(self):
        return self.name
    
class Ecu(models.Model):
    model = models.ForeignKey(EcuModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['model', 'number'], name='ecu_model_number_unique_constraint')
        ]
    
    def __str__(self):
        return self.number

class ConnectionTool(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name

class FileProcess(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class ProcessPricing(models.Model):
    process = models.ForeignKey(FileProcess, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'process'], name='processpricing_process_vehicle_unique_constraint')
        ]

class FileRequest(models.Model):
    transmissin_choices = [
        ("A", "AUTO"),
        ("M", "MANUAL")
    ]

    file_type_choices = [
        ("E", "ECU file"),
        ("T", "Transmission File")
    ]
    tool_type_choices = [
        ("S", "Slave"),
        ("M", "Master")
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    engine = models.ForeignKey(VehicleEngine, on_delete=models.PROTECT)
    ecu = models.ForeignKey(EcuModel, on_delete=models.PROTECT)

    file_type = models.CharField(max_length=1, choices=file_type_choices)
    transmissin = models.CharField(max_length=1, choices=transmissin_choices)
    tool = models.ForeignKey(ConnectionTool, on_delete=models.PROTECT)
    tool_type = models.CharField(max_length=1, choices=tool_type_choices)
    
    processes = models.ManyToManyField(FileProcess)
    customer_description = models.TextField(max_length=400)
    total_price = models.IntegerField()

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to="uploads/original/")
    
    employee_description = models.TextField(max_length=400, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)
    processed_file = models.FileField(upload_to="uploads/processed/", null=True, blank=True)
    
class Knowledge(models.Model):
    title = models.CharField(max_length=100, unique=True)
    link = models.URLField(null=True, blank=True)
    link_title = models.CharField(max_length=60, null=True, blank=True)
    desc = models.TextField(max_length=600, null=True, blank=True)
    
    def __str__(self):
        return self.title

class KnowledgePart(models.Model):
    title = models.CharField(max_length=100)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'knowledge'], name='knowledgepart_title_knowledge_unique_constraint')
        ]
    
    def __str__(self):
        return self.title + " - " + str(self.knowledge)

class KnowledgeBullet(models.Model):
    content = models.CharField(max_length=100)
    part = models.ForeignKey(KnowledgePart, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['content', 'part'], name='knowledgebullet_content_part_unique_constraint')
        ]

class DtcInfo(models.Model):
    code = models.CharField(max_length=7, unique=True)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class FileSale(models.Model):
    title = models.CharField(max_length=60, unique=True)
    file = models.FileField(upload_to="uploads/for_sale/", unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    desc = models.TextField(max_length=400)
    price = models.IntegerField()
    owners = models.ManyToManyField(Customer, blank=True)
    
    def __str__(self):
        return self.title

class Transaction(models.Model):
    transaction_type_choices = [
        ("E", "Expense"),
        ("D", "Deposit")
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=transaction_type_choices)
    
    file_request = models.OneToOneField(FileRequest, on_delete=models.CASCADE, null=True, blank=True)
    file_bought = models.OneToOneField(FileSale, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.IntegerField()
