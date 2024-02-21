from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View, DetailView, CreateView
from .models import RentContract, PayingDates
from apartment.models import Apartment
# Create your views here.



class CreateContractView(CreateView):
    model = RentContract
    template_name = 'rent_contract/create-rent-contract.html' 
    fields = ['apartment', 'tenant_name', 'tenant_phone_number', 
              'rent_price', 'notify_me', 'contract_photo', 'duration_in_months', 'notes', 
              ]
    

def mark_as_paid_unpaid(request, id):
    pay_date = get_object_or_404(PayingDates, pk=id)
    if request.method == 'PUT' and \
                    pay_date.contract.apartment.owner == request.user:        
        pay_date.is_paid = not pay_date.is_paid
        pay_date.save() 
    context = {}
    context['paying_dates'] = PayingDates.objects.filter(contract=pay_date.contract)
    return render(request, 'apartments/components/show_paying_dates.html', context)

def cancel_contract(request, pk):
    context = {}
    if request.method == "DELETE":
        # pk: rent-contract-id.
        current_contract = get_object_or_404(RentContract, pk=pk)
        current_contract.cancelContract()
        context['apartment'] = current_contract.apartment
        context['paying_dates'] = context['apartment'].get_contract_paying_dates()
        

    return render(request, 'apartments/components/view_apart_header.html', context)