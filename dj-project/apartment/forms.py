from django import forms
from .models import Apartment

class AddApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment 
        fields = ('country', 'city', 'price', 'notes')
    

# s.Model): 
    # owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # price = models.IntegerField()
    # country = models.CharField(max_length=20)
    # city = models.CharField(max_length=20)
    # rent_price = models.IntegerField()
    # currently_rented = models.BooleanField(default=False) 
    # notes = models.TextField(blank=True)
    # # public_visibility = models.BooleanField(default=False)
    # def __str__(self):
    #     return f"{self.country},  {self.city}" 
