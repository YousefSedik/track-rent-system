from django.db import models
from apartment.models import Apartment
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class RentContract(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant_name = models.CharField(max_length=100)
    tenant_phone_number = PhoneNumberField()
    rent_price = models.IntegerField()
    start_rent_date = models.DateField()
    duration_in_months = models.PositiveSmallIntegerField(default = 6, validators=[
        MaxValueValidator(12), MinValueValidator(1), 
    ])
    end_rent_date = models.DateField(null=True)
    notify_me = models.BooleanField(default=True)
    contract_photo = models.ImageField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.tenant_name + self.notes 
    
        
