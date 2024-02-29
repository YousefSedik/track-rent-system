from django.urls import path
from . import views
app_name = 'apartment'
urlpatterns = [
    path('', views.ApartmentView.as_view(), name='home'), 
    path('view/<int:pk>', views.ViewApartmentView.as_view(), name='view-apartment'), 
    path('add/', views.AddApartmentView.as_view(), name='add-apartment'), 
    path('edit/<int:pk>', views.EditApartmentView.as_view(), name='edit-apartment'), 
    path('delete/<int:pk>',views.DeleteApartmentView.as_view(), name='delete-apartment'), 
    path('AddMedia/<int:pk>', views.AddMediaView.as_view(), name='add_media_page'),
    
]


htmx_urlpatterns = [
    path('reversePublicity/<int:pk>', views.ReversePublicityView.as_view(), name='reversePublicity'),
    path('add-media/<int:pk>', views.AddMediaObjectView.as_view(), name='add-media' ),
    path('delete-media/<int:pk>', views.DeleteMediaView.as_view(), name='delete_media'),
    
]

urlpatterns += htmx_urlpatterns