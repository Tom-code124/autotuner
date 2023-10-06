from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+905551234567'. Up to 15 digits allowed.")

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    credit_amount = models.IntegerField(default=0)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class VehicleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

class VehicleBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

class EngineVersion(models.Model):
    name = models.CharField(max_length=100)

class VehicleModel(models.Model):
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='brand')
    versions = models.ManyToManyField(EngineVersion)

class Vehicle(models.Model):
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name='category')
    model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True, related_name='model')
    version = models.ForeignKey(EngineVersion, on_delete=models.SET_NULL, null=True, related_name='version')
    hp = models.IntegerField()
    year = models.IntegerField()

class EcuBrand(models.Model):
    name = models.CharField(max_length=50)

class EcuModel(models.Model):
    name = models.CharField(max_length=50)

class Ecu(models.Model):
    brand = models.ForeignKey(EcuBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(EcuModel, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    car_brands = models.ManyToManyField(VehicleBrand)

class FileRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    original_file = models.FileField(upload_to="uploads/original/")
    
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    processed_file = models.FileField(upload_to="uploads/processed/", null=True)
