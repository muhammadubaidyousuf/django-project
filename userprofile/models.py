from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import geocoder
g = geocoder.ip('me')
location = g.address

class UserInformationExt(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    full_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phno = models.CharField(max_length=15)
    user_address = models.CharField(default=location, max_length=100, null=True)
    user_location = models.CharField(max_length=100, null=True)
    user_profile_image = models.ImageField(upload_to='avatar/img', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.user_profile_image.path)
            if img.height > 300 or img.weight > 300:
                output_size = (170,170)
                img.thumbnail(output_size)
                img.save(self.user_profile_image.path)
        except ValueError:
            print("ValueError")