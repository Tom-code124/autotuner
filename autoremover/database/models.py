from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+905551234567'. Up to 15 digits allowed.")
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
transaction_type_choices = [
    ("E", "Expense"),
    ("D", "Deposit")
]
fuel_type_choices = [
    ("P", "Petrol"),
    ("D", "Diesel")
]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex], max_length=16, unique=True)
    credit_amount = models.IntegerField(default=0)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class VehicleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

class VehicleBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

class VehicleModel(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name='category')
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='brand')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['brand', 'name'], name='vehicle_model_brand_unique_constraint')
        ]

class Vehicle(models.Model):
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, null=True, related_name='model')
    year = models.IntegerField()

class VehicleEngine(models.Model):
    name = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=1, choices=fuel_type_choices)
    hp = models.IntegerField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='model')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'name', 'hp'], name='vehicle_name_hp_unique_constraint')
        ]

class EcuBrand(models.Model):
    name = models.CharField(max_length=50)

class EcuModel(models.Model): # for ecu type
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(EcuBrand, on_delete=models.CASCADE)

class Ecu(models.Model):
    model = models.ForeignKey(EcuModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    vehicles = models.ManyToManyField(Vehicle)

class ConnectionTool(models.Model):
    name = models.CharField(max_length=30)

class FileProcess(models.Model): # burada kaldım
    name = models.CharField(max_length=50)

class ProcessPricing(models.Model):
    process = models.ForeignKey(FileProcess, on_delete=models.CASCADE, related_name='process')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle')
    price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'process'], name='process_vehicle_unique_constraint')
        ]

class FileRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    processes = models.ManyToManyField(FileProcess)
    total_price = models.IntegerField()
    file_type = models.CharField(max_length=1, choices=file_type_choices)
    transmissin = models.CharField(max_length=1, choices=transmissin_choices)
    tool = models.ForeignKey(ConnectionTool, on_delete=models.SET_NULL, null=True, related_name='tool')
    tool_type = models.CharField(max_length=1, choices=tool_type_choices)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    original_file = models.FileField(upload_to="uploads/original/")
    
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    processed_file = models.FileField(upload_to="uploads/processed/", null=True, blank=True)
    
class Knowledge(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=400, null=True)

class KnowledgePart(models.Model):
    title = models.CharField(max_length=100)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)

class KnowledgeItem(models.Model):
    content = models.TextField(max_length=400)
    part = models.ForeignKey(KnowledgePart, on_delete=models.CASCADE)

class DtcInfo(models.Model):
    code = models.CharField(max_length=7)
    desc = models.CharField(max_length=100)

class FileSale(models.Model):
    file = models.FileField(upload_to="uploads/for_sale/")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    desc = models.TextField(max_length=400)
    price = models.IntegerField()
    owners = models.ManyToManyField(Customer)

class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=1, choices=transaction_type_choices)
    amount = models.IntegerField()
    file_request = models.OneToOneField(FileRequest, on_delete=models.CASCADE)
    file_bought = models.OneToOneField(FileSale, on_delete=models.CASCADE)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

