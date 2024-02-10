from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
# from django.views.generic.edit import
from django.db.models import OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Apartment, Photo, Video
from django.contrib.auth import get_user_model
from . import forms
# Create your views here.


class ApartmentView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = Apartment 
    template_name = 'apartments/home.html'
    context_object_name = 'apartment_list' 
    def get_queryset(self):
        queryset = super(ApartmentView, self).get_queryset()
        return queryset
class ViewApartmentView(DetailView):
    model = Apartment 
    template_name = 'apartments/view_apart.html'
    context_object_name = 'apartment'
    
    def get_queryset(self):
        return Apartment.objects.filter(pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(apartment=context['apartment'])
        context['videos'] = Video.objects.filter(apartment=context['apartment'])
        return context
class AddApartmentView(LoginRequiredMixin, CreateView): 
    login_url = "/login/"
    form_class = forms.AddApartmentForm
    template_name = 'apartments/add_apartment.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddApartmentView, self).form_valid(form)
    
    

class EditApartmentView(UpdateView, LoginRequiredMixin):
    login_url = "/login/"
    template_name = 'apartments/edit_apart.html'
    model = Apartment
    fields = [ 
        "country", 
        "city",
        "notes",
        "rent_price",
    ] 
    success_url ="/"


def reverse_public_visibility(request, pk):
    apartment = Apartment.objects.get(pk=pk)
    if request.htmx and request.user == apartment.owner:
        apartment.reverse_public_visibility()
    return HttpResponse('')
   
        
        
def delete_apartment(request, pk):
    apartment = Apartment.objects.get(pk=pk)
    if request.user == apartment.owner:
        apartment.delete()
    response = HttpResponse()
    response["HX-Redirect"] = "/"
    return response
