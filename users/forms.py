from . import models
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from users.models import CustomUser
fields = ('email', 'phone_number','name', 'password1', 'password2')
class CustomUserCreationForm(UserCreationForm): 
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = CustomUser 
        fields = fields
        
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = CustomUser.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email
    
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = CustomUser.objects.create_user(  
            self.cleaned_data['email'],  
            self.cleaned_data['password1'],
            phone_number = self.cleaned_data['phone_number'],  
            name = self.cleaned_data['name'],  
        )  
        return user  

class CustomLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':"form-control"
    }))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class':"form-control"
    }))
