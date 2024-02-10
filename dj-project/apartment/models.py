from django.db import models
from users.models import CustomUser

class Apartment(models.Model): 
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField()
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    rent_price = models.IntegerField(null=True)
    currently_rented = models.BooleanField(default=False) 
    notes = models.TextField(blank=True)
    public_visibility = models.BooleanField(default=False)
    
    def reverse_public_visibility(self):
        self.public_visibility = not self.public_visibility
        self.save()
    
    def __str__(self):
        return f"{self.country}, {self.city}" 

class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='photos', default=1)
    
    def __str__(self):
        return f'Photo Added At {self.date_added}'

class Video(models.Model):
    video = models.FileField(upload_to='videos/', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='videos', default=1)

    def __str__(self):
        return f'Video Added At {self.date_added}'
