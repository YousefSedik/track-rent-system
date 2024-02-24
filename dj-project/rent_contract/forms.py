from django import forms
from .models import RentContract
class AddRentContractForm(forms.ModelForm):
    class Meta:
        model = RentContract    
        fields = [
            'tenant_name',
            'tenant_phone_number',
            'rent_price',
            'duration_in_months',
            'notify_me',
            'contract_photo',
            'notes',
        ]
        