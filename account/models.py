from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import geocoder
g = geocoder.ip('me')
# Create your models here.


class UserExtData(models.Model):
    phone_no = models.CharField(max_length=15)
    user_email = models.CharField(max_length=30)
    user_location = models.CharField(max_length=30)
    user_join_date = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class CarImages(models.Model):
    name_img = models.CharField(max_length=50)
    img_url = models.FileField(upload_to='account/media_files', blank=True)

    def __str__(self):
        return self.name_img


class UserAddCar(models.Model):
    c_title = models.CharField(max_length=100)
    c_car_name = models.CharField(max_length=25)
    c_car_color = models.CharField(max_length=20)
    c_par_day_price = models.CharField(max_length=50)
    c_car_model = models.CharField(max_length=25)
    c_address = models.CharField(max_length=50)
    c_car_plate = models.CharField(max_length=50)
    c_self_driver = models.CharField(max_length=5)
    c_car_about = models.TextField(max_length=300)
    c_let_1 = models.CharField(max_length=150)
    c_log_2 = models.CharField(max_length=150)
    c_select_image = models.URLField()
    c_date_time = models.DateField(default=now)
    c_user_state = models.TextField(g.state, default='SOME STRING')
    c_user_city = models.TextField(g.city, default='SOME STRING')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)



