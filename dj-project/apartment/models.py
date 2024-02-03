from django.db import models
from users.models import CustomUser
# Create your models here.


class Apartment(models.Model): 
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField()
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    # gmaps = models.CharField(max_length=20)
    rent_price = models.IntegerField()
    currently_rented = models.BooleanField(default=False) 
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.country},  {self.city}" 

class ApartmentMedia(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.apartment} Media."
    
class Photo(models.Model):
    photo = models.ImageField(upload_to='media/photos')
    date_added = models.DateTimeField(auto_now_add=True)
    apart_media = models.ForeignKey(ApartmentMedia, on_delete=models.CASCADE)
    def __str__(self):
        return f'Photo Added At {self.date_added}'
class Video(models.Model):
    video = models.FileField(upload_to='media/videos')
    date_added = models.DateTimeField(auto_now_add=True)
    apart_media = models.ForeignKey(ApartmentMedia, on_delete=models.CASCADE)
    def __str__(self):
        return f'Video Added At {self.date_added}'