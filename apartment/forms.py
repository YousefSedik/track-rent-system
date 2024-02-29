from django import forms
from .models import Apartment

class AddApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment 
        fields = ('country', 'city', 'price', 'notes')
    

