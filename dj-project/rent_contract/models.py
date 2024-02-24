from django.db import models
from apartment.models import Apartment
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from dateutil.relativedelta import relativedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

class PayingDates(models.Model):
    
    month_counter = models.SmallIntegerField()
    date = models.DateField()
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    contract = models.ForeignKey('RentContract', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.contract.tenant_name}, rented {self.contract.apartment}"

class RentContract(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant_name = models.CharField(max_length=100)
    tenant_phone_number = PhoneNumberField(null=True, blank=True)
    rent_price = models.IntegerField(null=True)
    start_rent_date = models.DateField(auto_now_add=True)
    duration_in_months = models.PositiveSmallIntegerField(default = 6, validators=[
        MaxValueValidator(12), MinValueValidator(1), 
    ])
    notify_me = models.BooleanField(default=True)
    contract_photo = models.ImageField(null=True, blank=True, upload_to='photos/')
    notes = models.TextField(null=True, blank=True)

    def generatePayingDates(self):
        add_date = relativedelta(months=1)
        date = self.start_rent_date
        for counter in range(self.duration_in_months):
            PayingDates.objects.create(month_counter=counter + 1, date=date, contract=self)
            date += add_date
    
    def send_message(self):
        pass
    
    def cancelContract(self):
        'Setting the rest of the months as canceled'
         
        associatedPayingDates = PayingDates.objects.filter(contract=self) 
        for month in associatedPayingDates:
            if not month.is_paid:
                month.is_canceled = True
                month.save()
        self.apartment.is_rented = False
        self.apartment.save()
            
    def __str__(self):
        return self.tenant_name + self.notes 
    
    
@receiver(pre_delete, sender=RentContract)
def delete_paying_dates(instance, *args, **kwargs):
    instance.cancelContract()

@receiver(post_save, sender=RentContract)
def post_save_generate(created, instance, *args, **kwargs):
    if created:
        instance.generatePayingDates()
        

@receiver(pre_save, sender=RentContract)
def can_be_rented(instance, **kwargs):
    if not instance.apartment.is_rented and instance.id is None:
        instance.apartment.is_rented = True
        if instance.rent_price:
            instance.apartment.rent_price = instance.rent_price

        instance.apartment.save()

    elif instance.apartment.is_rented:
        raise RuntimeError("Apartment Can't have 2 contracts in the same time.")
