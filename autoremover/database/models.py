from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from datetime import datetime
from dateutil import relativedelta

class Customer(models.Model):
    phone_regex_validator = RegexValidator(regex=r'^[0-9]{7,13}$', message="Up to 13 digits allowed for phone number. (Except phone zone)")
    phone_zone_choices = [('+1', 'Canada +1'), ('+7', 'Kazakhstan +7'), ('+20', 'Egypt +20'), ('+27', 'South Africa +27'), ('+30', 'Greece +30'), ('+31', 'Netherlands +31'), ('+32', 'Belgium +32'), ('+33', 'France +33'), ('+34', 'Spain +34'), ('+36', 'Hungary +36'), ('+39', 'Italy +39'), ('+40', 'Romania +40'), ('+41', 'Switzerland +41'), ('+43', 'Austria +43'), ('+44', 'United Kingdom +44'), ('+45', 'Denmark +45'), ('+46', 'Sweden +46'), ('+47', 'Norway +47'), ('+48', 'Poland +48'), ('+49', 'Germany +49'), ('+51', 'Peru +51'), ('+52', 'Mexico +52'), ('+53', 'Cuba +53'), ('+54', 'Argentina +54'), ('+55', 'Brazil +55'), ('+56', 'Chile +56'), ('+57', 'Colombia +57'), ('+58', 'Venezuela +58'), ('+60', 'Malaysia +60'), ('+61', 'Australia +61'), ('+62', 'Indonesia +62'), ('+63', 'Philippines +63'), ('+64', 'New Zealand +64'), ('+65', 'Singapore +65'), ('+66', 'Thailand +66'), ('+81', 'Japan +81'), ('+82', 'South Korea +82'), ('+84', 'Vietnam +84'), ('+86', 'China +86'), ('+90', 'Türkiye +90'), ('+91', 'India +91'), ('+92', 'Pakistan +92'), ('+93', 'Afghanistan +93'), ('+94', 'Sri Lanka +94'), ('+95', 'Myanmar +95'), ('+98', 'Iran +98'), ('+211', 'South Sudan +211'), ('+212', 'Morocco +212'), ('+213', 'Algeria +213'), ('+216', 'Tunisia +216'), ('+218', 'Libya +218'), ('+220', 'Gambia +220'), ('+221', 'Senegal +221'), ('+222', 'Mauritania +222'), ('+223', 'Mali +223'), ('+224', 'Guinea +224'), ('+225', 'Ivory Coast +225'), ('+226', 'Burkina Faso +226'), ('+227', 'Niger +227'), ('+228', 'Togo +228'), ('+229', 'Benin +229'), ('+230', 'Mauritius +230'), ('+231', 'Liberia +231'), ('+232', 'Sierra Leone +232'), ('+233', 'Ghana +233'), ('+234', 'Nigeria +234'), ('+235', 'Chad +235'), ('+236', 'Central African Republic +236'), ('+237', 'Cameroon +237'), ('+238', 'Cape Verde +238'), ('+239', 'Sao Tome and Principe +239'), ('+240', 'Equatorial Guinea +240'), ('+241', 'Gabon +241'), ('+242', 'Republic of the Congo +242'), ('+243', 'Democratic Republic of the Congo +243'), ('+244', 'Angola +244'), ('+245', 'Guinea-Bissau +245'), ('+246', 'British Indian Ocean Territory +246'), ('+248', 'Seychelles +248'), ('+249', 'Sudan +249'), ('+250', 'Rwanda +250'), ('+251', 'Ethiopia +251'), ('+252', 'Somalia +252'), ('+253', 'Djibouti +253'), ('+254', 'Kenya +254'), ('+255', 'Tanzania +255'), ('+256', 'Uganda +256'), ('+257', 'Burundi +257'), ('+258', 'Mozambique +258'), ('+260', 'Zambia +260'), ('+261', 'Madagascar +261'), ('+262', 'Mayotte +262'), ('+263', 'Zimbabwe +263'), ('+264', 'Namibia +264'), ('+265', 'Malawi +265'), ('+266', 'Lesotho +266'), ('+267', 'Botswana +267'), ('+268', 'Swaziland +268'), ('+269', 'Comoros +269'), ('+290', 'Saint Helena +290'), ('+291', 'Eritrea +291'), ('+297', 'Aruba +297'), ('+298', 'Faroe Islands +298'), ('+299', 'Greenland +299'), ('+350', 'Gibraltar +350'), ('+351', 'Portugal +351'), ('+352', 'Luxembourg +352'), ('+353', 'Ireland +353'), ('+354', 'Iceland +354'), ('+355', 'Albania +355'), ('+356', 'Malta +356'), ('+357', 'Cyprus +357'), ('+358', 'Finland +358'), ('+359', 'Bulgaria +359'), ('+370', 'Lithuania +370'), ('+371', 'Latvia +371'), ('+372', 'Estonia +372'), ('+373', 'Moldova +373'), ('+374', 'Armenia +374'), ('+375', 'Belarus +375'), ('+376', 'Andorra +376'), ('+377', 'Monaco +377'), ('+378', 'San Marino +378'), ('+379', 'Vatican +379'), ('+380', 'Ukraine +380'), ('+381', 'Serbia +381'), ('+382', 'Montenegro +382'), ('+383', 'Kosovo +383'), ('+385', 'Croatia +385'), ('+386', 'Slovenia +386'), ('+387', 'Bosnia and Herzegovina +387'), ('+389', 'Macedonia +389'), ('+420', 'Czech Republic +420'), ('+421', 'Slovakia +421'), ('+423', 'Liechtenstein +423'), ('+500', 'Falkland Islands +500'), ('+501', 'Belize +501'), ('+502', 'Guatemala +502'), ('+503', 'El Salvador +503'), ('+504', 'Honduras +504'), ('+505', 'Nicaragua +505'), ('+506', 'Costa Rica +506'), ('+507', 'Panama +507'), ('+508', 'Saint Pierre and Miquelon +508'), ('+509', 'Haiti +509'), ('+590', 'Saint Barthelemy +590'), ('+591', 'Bolivia +591'), ('+592', 'Guyana +592'), ('+593', 'Ecuador +593'), ('+595', 'Paraguay +595'), ('+597', 'Suriname +597'), ('+598', 'Uruguay +598'), ('+599', 'Curacao +599'), ('+670', 'East Timor +670'), ('+672', 'Antarctica +672'), ('+673', 'Brunei +673'), ('+674', 'Nauru +674'), ('+675', 'Papua New Guinea +675'), ('+676', 'Tonga +676'), ('+677', 'Solomon Islands +677'), ('+678', 'Vanuatu +678'), ('+679', 'Fiji +679'), ('+680', 'Palau +680'), ('+681', 'Wallis and Futuna +681'), ('+682', 'Cook Islands +682'), ('+683', 'Niue +683'), ('+685', 'Samoa +685'), ('+686', 'Kiribati +686'), ('+687', 'New Caledonia +687'), ('+688', 'Tuvalu +688'), ('+689', 'French Polynesia +689'), ('+690', 'Tokelau +690'), ('+691', 'Micronesia +691'), ('+692', 'Marshall Islands +692'), ('+850', 'North Korea +850'), ('+852', 'Hong Kong +852'), ('+853', 'Macao +853'), ('+855', 'Cambodia +855'), ('+856', 'Laos +856'), ('+880', 'Bangladesh +880'), ('+886', 'Taiwan +886'), ('+960', 'Maldives +960'), ('+961', 'Lebanon +961'), ('+962', 'Jordan +962'), ('+963', 'Syria +963'), ('+964', 'Iraq +964'), ('+965', 'Kuwait +965'), ('+966', 'Saudi Arabia +966'), ('+967', 'Yemen +967'), ('+968', 'Oman +968'), ('+970', 'Palestine +970'), ('+971', 'United Arab Emirates +971'), ('+972', 'Israel +972'), ('+973', 'Bahrain +973'), ('+974', 'Qatar +974'), ('+975', 'Bhutan +975'), ('+976', 'Mongolia +976'), ('+977', 'Nepal +977'), ('+992', 'Tajikistan +992'), ('+993', 'Turkmenistan +993'), ('+994', 'Azerbaijan +994'), ('+995', 'Georgia +995'), ('+996', 'Kyrgyzstan +996'), ('+998', 'Uzbekistan +998')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_zone = models.CharField(choices=phone_zone_choices, default='+90')
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=16)
    credit_amount = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_zone', 'phone_number'], name='customer_phonezone_phonenumber_unique_constraint')
        ]

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
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
    
class ConnectionTool(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name
    
class VehiclePotential(models.Model):
    old_hp = models.PositiveIntegerField()
    new_hp = models.PositiveIntegerField()
    old_nm = models.PositiveIntegerField()
    new_nm = models.PositiveIntegerField()
    known_reading_methods = models.ManyToManyField(ConnectionTool)
    
class Vehicle(models.Model):
    vehicle_year = models.ForeignKey(VehicleYear, on_delete=models.CASCADE)
    version = models.ForeignKey(VehicleVersion, on_delete=models.PROTECT)
    ecu_model = models.ForeignKey(EcuModel, on_delete=models.PROTECT)
    potential = models.OneToOneField(VehiclePotential, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicle")

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
    price = models.FloatField()

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
        
        for process in self.processes.all():
            total += ProcessPricing.objects.get(vehicle=self.vehicle, process=process).price

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
    
    def add_process(self, process):
        self.processes.add(process)

        self.transaction.amount = self.total_price
        self.transaction.save()
        
    def remove_process(self, process):
        if process in self.processes.all():
            self.processes.remove(process)

            self.transaction.amount = self.total_price
            self.transaction.save()

@receiver(post_save, sender=FileRequest, dispatch_uid="update_transaction")
def create_transaction(sender, instance, **kwargs):
    transaction, created = Transaction.objects.get_or_create(
        customer=instance.customer,
        file_request=instance,
        defaults={'amount': instance.total_price, "type": "E"}
        )

@receiver(m2m_changed, sender=FileRequest.processes.through)
def update_transaction(sender, instance, **kwargs):
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

    @property
    def status(self):
        if self.is_scheduled:
            now = datetime.now()
            for schedule in self.file_service_schedule_set.all():
                if now.strftime("%a") == schedule.day and int(now.strftime("%H")) >= schedule.starting_hour and int(now.strftime("%H")) < schedule.ending_hour:
                    return "ONLINE"
        else:
            if self.is_online:
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
                d.replace(hour=s.starting_hour, minute=0)

                nd = today + relativedelta.relativedelta(weeks=1, weekday=days[s.day])
                nd.replace(hour=s.starting_hour, minute=0)

                l.append(d)
                l.append(nd)

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
                d.replace(hour=s.ending_hour, minute=0)

                nd = today + relativedelta.relativedelta(weeks=1, weekday=days[s.day])
                nd.replace(hour=s.ending_hour, minute=0)

                l.append(d)
                l.append(nd)

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
