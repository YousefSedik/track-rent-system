from django.urls import path
from . import views
app_name = 'apartment'
urlpatterns = [
    path('', views.ApartmentView.as_view(), name='home'), 
    path('view/<int:pk>', views.ViewApartmentView.as_view(), name='view-apartment'), 
    path('add/', views.AddApartmentView.as_view(), name='add-apartment'), 
    path('edit/<int:pk>', views.EditApartmentView.as_view(), name='edit-apartment'), 
    path('delete/<int:pk>',views.delete_apartment, name='delete-apartment'), 
    
]


htmx_urlpatterns = [
    path('reversePublicity/<int:pk>', views.reverse_public_visibility, name='reversePublicity'),
]

urlpatterns += htmx_urlpatterns