from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

class Apartment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField()
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    rent_price = models.IntegerField(null=True)
    notes = models.TextField(blank=True)
    public_visibility = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)
    
    def reverse_public_visibility(self):
        self.public_visibility = not self.public_visibility
        self.save()

    def delete_all_media(self):    
        Video.objects.filter(apartment=self).delete()

    def get_contract_paying_dates(self):
        contract = self.rentcontract_set.all().order_by('-id').first()
        if contract:
            return contract.payingdates_set.all()
        return None
        
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



@receiver(post_delete, sender=Photo)
@receiver(post_delete, sender=Video)
def delete_media_file(sender, instance, **kwargs):
    if isinstance(instance, Photo):
        if instance.photo:
            instance.photo.delete(save=False)
    elif isinstance(instance, Video):
        if instance.video:
            instance.video.delete(save=False)
