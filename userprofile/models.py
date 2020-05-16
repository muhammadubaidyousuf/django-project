from django.db import models
from django.contrib.auth.models import User
import geocoder
g = geocoder.ip('me')
location = g.address


class UserInformationExt(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    full_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phno = models.CharField(max_length=15)
    user_profile_image = models.ImageField(upload_to='avatar/img', null=True)
    user_address = models.CharField(default=location, max_length=100)
    user_location = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
