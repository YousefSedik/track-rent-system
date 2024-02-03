from django.shortcuts import render, redirect
from . import forms
from django.views.generic import CreateView, FormView, View
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignUpView(LoginRequiredMixin, View):
    redirect_authenticated_user = True  

    def get(self, request, *args, **kwargs):
        context = {
            'form': forms.CustomUserCreationForm()
        }
        return render(request, 'users/sign-up.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = forms.CustomUserCreationForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        
        return render(request, 'users/sign-up.html', context=context)
        


class LoginView(LoginRequiredMixin, View):
    redirect_authenticated_user = True  
    def get(self, request, *args, **kwargs):
        context = {
            'form':forms.CustomLoginForm()
        }
        return render(request, 'users/login.html', context=context)
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        user = authenticate(email=email, password=password)
        if user:
            login(request, user) 
            return redirect('/')
        else:
            messages.error(request, 'email or the password are not valid. ')
            newForm = forms.CustomLoginForm(request.POST or None)
            context = {
                'form': newForm
            }
            return render(request, 'users/login.html', context=context)
        

def Logout(request):
    if request.user.is_authenticated():
        logout(request)
    else:
        return redirect('/')