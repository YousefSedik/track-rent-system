from django import forms
from .models import RentContract
class AddRentContractForm(forms.ModelForm):
    model = RentContract()
    class Meta:
        fields = [
            tenant_name,
            tenant_phone_number,
            rent_price,
            start_rent_date, 
            contract_duration, 
            notify_me,
            contract_photo,
            notes,
        ]
    
    
# class RentContract(models.Model):
#     apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
#     tenant_name = models.CharField(max_length=100)
#     tenant_phone_number = PhoneNumberField()
#     rent_price = models.IntegerField()
#     start_rent_date = models.DateField()
#     contract_duration = models.DurationField()
#     notify_me = models.BooleanField(default=True)
#     contract_photo = models.ImageField(default='media/')
#     notes = models.TextField(blank=True)
    