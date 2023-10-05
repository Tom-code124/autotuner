from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    credit_amount = models.IntegerField()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class VehicleCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

class VehicleBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Vehicle(models.Model):
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name='category')
    brand = models.ForeignKey(VehicleBrand, on_delete=models.SET_NULL, null=True, related_name='brand')


class FileRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    original_file = models.FileField(upload_to="uploads/original/")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    processed_file = models.FileField(upload_to="uploads/processed/", null=True)
