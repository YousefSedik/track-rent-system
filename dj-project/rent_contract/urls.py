from django.urls import path
from . import views
app_name = 'rent_contract'

urlpatterns = [
    path('create-contract/', views.CreateContractView.as_view(), name='create-contract')
]

htmx_urlpatterns = [
    path('mark/<int:id>', views.mark_as_paid_unpaid, name='mark_as_paid_unpaid'),
    path('cancel_contract/<int:pk>', views.cancel_contract, name='cancel_contract'),
]
    
urlpatterns += htmx_urlpatterns
