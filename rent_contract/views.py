from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View, DetailView, CreateView
from .models import RentContract, PayingDates
from apartment.models import Apartment
from users.models import CustomUser
from django.http.response import HttpResponse
from django.contrib import messages
from . import forms

# Create your views here.


class CreateContractView(CreateView):
    form_class = forms.AddRentContractForm
    template_name = 'rent_contract/create-rent-contract.html' 
    success_url = '/'
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        pk = self.kwargs['pk']
        apartment = get_object_or_404(Apartment, pk=pk)
        form.instance.apartment = apartment
        if self.request.user != apartment.owner:
            raise Exception('self.request.user != apartment.owner')
        return super().form_valid(form)
    
class ContractDetailView(DetailView):
    context_object_name = 'contract'
    model = RentContract
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == context['contract'].apartment.owner:         
            context['paying_dates'] = PayingDates.objects.filter(contract=context['contract'])
        else:
            context = {}
        return context

class MarkAsPaidUnpaidView(View):
    def put(self, request, *args, **kwargs):
        pay_date = get_object_or_404(PayingDates, pk=kwargs['id'])
        if request.method == 'PUT' and \
                        pay_date.contract.apartment.owner == request.user:  
                            
            associated_pay_dates = PayingDates.objects.filter(contract=pay_date.contract)
            for i in associated_pay_dates:
                if pay_date.is_paid and i.id >= pay_date.id:
                    i.is_paid = False
                    i.save()
                elif not pay_date.is_paid and i.id <= pay_date.id:
                    i.is_paid = True
                    i.save()

            context = {}
            context['paying_dates'] = associated_pay_dates
        return render(request, 'apartments/components/show_paying_dates.html', context)

class CancelContractView(View):
    def delete(self, request, *args, **kwargs):
        context = {}
        current_contract = get_object_or_404(RentContract, pk=kwargs['pk'])
        if request.method == "DELETE" and current_contract.apartment.owner == request.user:
            # pk: rent-contract-id.
            current_contract.cancelContract()
            context['apartment'] = current_contract.apartment
            context['paying_dates'] = context['apartment'].get_contract_paying_dates()

        return render(request, 'apartments/components/view_apart_header.html', context)

class ViewTrackRent(ListView):
    model = RentContract
    template_name = 'rent_contract/track-rent.html'
    context_object_name = 'pay_dates'
    paginate_by = 15
    def get_queryset(self):
        # After Optimization:

        queryset = super(ViewTrackRent, self).get_queryset()
        pay_dates = PayingDates.objects.filter(contract__in = queryset).select_related('contract')
        
        # Before:

        # queryset = RentContract.objects.filter(apartment__owner = self.request.user)
        # pay_dates = PayingDates.objects.none()
        # for contract in queryset:
        #     pay_dates |= PayingDates.objects.filter(contract=contract)
        # pay_dates = pay_dates.order_by('date')
        
        return pay_dates