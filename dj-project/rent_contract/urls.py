from django.urls import path
from . import views
app_name = 'rent_contract'

urlpatterns = [
    path('create-contract/<int:pk>', views.CreateContractView.as_view(), name='create-contract'),
    path('contract-details/<int:pk>', views.ContractDetailView.as_view(), name='contract-details'),
    path('track-rent/', views.ViewTrackRent.as_view(), name='track-rent')
]

htmx_urlpatterns = [
    path('mark/<int:id>', views.MarkAsPaidUnpaidView.as_view(), name='mark_as_paid_unpaid'),
    path('cancel_contract/<int:pk>', views.CancelContractView.as_view(), name='cancel_contract'),
]
    
urlpatterns += htmx_urlpatterns
