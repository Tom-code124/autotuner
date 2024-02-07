from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from datetime import datetime
from dateutil import relativedelta

class Customer(models.Model):
    phone_regex_validator = RegexValidator(regex=r'^[\+][0-9]{9,20}$', message="Starts with + (include country code) and no spaces etc. allowed!")
    pricing_class_choices = [
        ("M", "Master"),
        ("S", "Slave"),
        ("E", "Euro"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=20, unique=True)
    credit_amount = models.FloatField(default=0)
    pricing_class = models.CharField(max_length=1, choices=pricing_class_choices, default="E")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=Employee, dispatch_uid="add_permission_group")
def create_transaction(sender, instance, **kwargs):
    g = Group.objects.get(name="employee_permission_group")
    instance.user.groups.add(g)
    instance.user.is_staff = True
    instance.user.save()

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

class FileProcess(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class ProcessPricing(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    process = models.ForeignKey(FileProcess, on_delete=models.CASCADE)
    master_price = models.FloatField()
    slave_price = models.FloatField()
    euro_price = models.FloatField()

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
        ("M", "Master"),
        ("E", "Euro"),
    ]

    status_choices = [
        ("D", "Done"),
        ("C", "Cancelled"),
        ("O", "Ongoing")
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    tool = models.ForeignKey(ConnectionTool, on_delete=models.PROTECT)
    processes = models.ManyToManyField(FileProcess)

    file_type = models.CharField(max_length=1, choices=file_type_choices)
    transmission = models.CharField(max_length=1, choices=transmissin_choices)
    tool_type = models.CharField(max_length=1, choices=tool_type_choices)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_description = models.TextField(max_length=400)
    original_file = models.FileField(upload_to="processing/original/")
    
    employee_description = models.TextField(max_length=400, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)
    processed_file = models.FileField(upload_to="processing/processed/", null=True, blank=True)

    status = models.CharField(max_length=1, choices=status_choices, default="O")

    @property
    def total_price(self):
        total = 0
        
        pricing_class = self.customer.pricing_class
        for process in self.processes.all():
            if pricing_class == "M":
                total += ProcessPricing.objects.get(vehicle=self.vehicle, process=process).master_price
            elif pricing_class == "S":
                total += ProcessPricing.objects.get(vehicle=self.vehicle, process=process).slave_price
            elif pricing_class == "E":
                total += ProcessPricing.objects.get(vehicle=self.vehicle, process=process).euro_price

        tax_percentage = SystemSetting.objects.all()[0].tax_percentage
        total *= 1 + (tax_percentage / 100)

        return total
    
    @property
    def processes_string(self):
        p_list = ""

        for process in self.processes.all():
            p_list += str(process) + ", "

        return p_list[0:-2]
    
    @property
    def status_long(self):
        return next((y for x, y in self.status_choices if x == self.status), None)

@receiver(post_save, sender=FileRequest, dispatch_uid="update_transaction")
def create_transaction(sender, instance, **kwargs):
    transaction, created = Transaction.objects.get_or_create(
        customer=instance.customer,
        file_request=instance,
        defaults={'amount': instance.total_price, "type": "E"}
        )
    
    if instance.status == "C":
        transaction.amount = 0
        transaction.save()
    else:
        transaction.amount = instance.total_price
        transaction.save()

@receiver(m2m_changed, sender=FileRequest.processes.through)
def update_transaction(sender, instance, **kwargs):
    if instance.status == "C":
        instance.transaction.amount = 0
        instance.transaction.save()
    else:
        instance.transaction.amount = instance.total_price
        instance.transaction.save()

            
class FileSale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80, unique=True)
    file = models.FileField(upload_to="sale/", unique=True)
    desc = models.TextField(max_length=600)
    price = models.FloatField()
    
    def __str__(self):
        return self.title + " filesale"
    
class FilePurchase(models.Model):
    bought_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file_sale = models.ForeignKey(FileSale, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'file_sale'], name='filepurchase_customer_filesale_unique_constraint')
        ]

class Transaction(models.Model):
    transaction_type_choices = [
        ("E", "Expense"),
        ("D", "Deposit")
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=transaction_type_choices, default="D")
    
    file_request = models.OneToOneField(FileRequest, on_delete=models.CASCADE, null=True, blank=True)
    file_bought = models.OneToOneField(FileSale, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.FloatField()

    @property
    def desc(self):
        if self.type == "D":
            return "You have deposited " + str(self.amount) + " credits."
        
        else:
            if self.file_request is not None:
                return 'You have requested: "' + self.file_request.processes_string + '" for ' + str(self.file_request.vehicle) + "."
            else:
                return "You have bought: " + str(self.file_bought)
            
    @property
    def category(self):
        if self.type == "D":
            return "Deposit"

        else:
            if self.file_request is not None:
                return "File request"
            
            else:
                return "File purchase"
    
    @property
    def type_long(self):
        return next((y for x, y in self.transaction_type_choices if x == self.type), None)

            
    def save(self, *args, **kwargs):
        already_exist = self.pk is not None
        if already_exist:
            old_amount = Transaction.objects.get(id=self.id).amount

        super(Transaction, self).save(*args, **kwargs)

        if self.pk is not None:
            if self.type == "D":
                if already_exist:
                    self.customer.credit_amount -= old_amount
                self.customer.credit_amount += self.amount
                self.customer.save()

            else:
                if already_exist:
                    self.customer.credit_amount += old_amount
                self.customer.credit_amount -= self.amount
                self.customer.save()
    
    def __str__(self):
        return self.type_long + " | " + str(self.customer) + " | " + str(self.id)

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

class KnowledgeAd(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

class DtcInfo(models.Model):
    code = models.CharField(max_length=7)
    desc = models.TextField(max_length=1000)

    def __str__(self):
        return self.code + " dtc"

class FileService(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    manual_status = models.BooleanField()
    is_scheduled = models.BooleanField()

    def __str__(self):
        return str(self.employee) + " file service settings"

    @property
    def status(self):
        if self.is_scheduled:
            now = datetime.now()
            for schedule in self.fileserviceschedule_set.all():
                if now.strftime("%a") == schedule.day and int(now.strftime("%H")) >= schedule.starting_hour and int(now.strftime("%H")) < schedule.ending_hour:
                    return "ONLINE"
        else:
            if self.manual_status:
                return "ONLINE"
        
        return "OFFLINE"
    
    @property
    def next_start(self):
        l = []
        today = datetime.now()

        if self.is_scheduled:
            days = {
                'Mon': 0,
                'Tue': 1,
                'Wed': 2,
                'Thu': 3,
                'Fri': 4,
                'Sat': 5,
                'Sun': 6
            }

            schedules = FileServiceSchedule.objects.filter(file_service=self)
            for s in schedules:
                d = today + relativedelta.relativedelta(weekday=days[s.day])
                l.append(d.replace(hour=s.starting_hour, minute=0, second=0, microsecond=0))

                nd = today + relativedelta.relativedelta(weeks=1, weekday=days[s.day])
                l.append(nd.replace(hour=s.starting_hour, minute=0, second=0, microsecond=0))

            l.sort()
            for d in l:
                if d > today:
                    return d

        return None
    
    @property
    def next_end(self):
        l = []
        today = datetime.now()

        if self.is_scheduled:
            days = {
                'Mon': 0,
                'Tue': 1,
                'Wed': 2,
                'Thu': 3,
                'Fri': 4,
                'Sat': 5,
                'Sun': 6
            }

            schedules = FileServiceSchedule.objects.filter(file_service=self)
            for s in schedules:
                d = today + relativedelta.relativedelta(weekday=days[s.day])
                l.append(d.replace(hour=s.ending_hour, minute=0, second=0, microsecond=0))

                nd = today + relativedelta.relativedelta(weeks=1, weekday=days[s.day])
                l.append(nd.replace(hour=s.ending_hour, minute=0, second=0, microsecond=0))

            l.sort()
            for d in l:
                if d > today:
                    return d

        return None


    @classmethod
    def system_status(cls):
        for instance in cls.objects.all():
            if instance.status == "ONLINE":
                return "ONLINE"
            
        return "OFFLINE"
    
    @classmethod
    def next_turn(cls):
        if cls.system_status() == "ONLINE":
            l = []
            for instance in cls.objects.all():
                ne = instance.next_end
                if ne is not None:
                    l.append(ne)
            
            if l:
                l.sort()
                return l[0]
            else:
                return None
        
        else:
            l = []
            for instance in cls.objects.all():
                ns = instance.next_start
                if ns is not None:
                    l.append(ns)
            
            if l:
                l.sort()
                return l[0]
            else:
                return None


class FileServiceSchedule(models.Model):
    day_choices = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday")
        ]

    day = models.CharField(max_length=3, choices=day_choices)
    starting_hour = models.PositiveIntegerField()
    ending_hour = models.PositiveIntegerField()
    file_service = models.ForeignKey(FileService, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_starting_hour_range",
                check=models.Q(starting_hour__range=(0, 24)),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_ending_hour_range",
                check=models.Q(ending_hour__range=(0, 24)),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_endinghour_greater_than_startinghour",
                check=models.Q(ending_hour__gt=models.F("starting_hour")),
            ),
            models.UniqueConstraint(
                fields=['file_service', 'day'],
                name='file_service_schedule_day_fileservice_unique_constraint'
            )
        ]

class SystemSetting(models.Model):
    tax_percentage = models.FloatField()
    iban_number = models.CharField(max_length=36)
    swift_number = models.CharField(max_length=12)
    bank_name = models.CharField(max_length=200)
    bank_account_owner_name = models.CharField(max_length=100)
    credit_try_price = models.FloatField(default=1)
    credit_eur_price = models.FloatField(default=1)

    def __str__(self):
        return "System settings"
