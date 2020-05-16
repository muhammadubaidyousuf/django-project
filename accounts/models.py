from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import geocoder
g = geocoder.ip('me')


class CarImages(models.Model):
    name_img = models.CharField(max_length=30)
    car_img = models.ImageField(upload_to='cars/img', null=True)


class UserBookCar(models.Model):
    full_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    message = models.TextField()
    post_title = models.CharField(max_length=100)
    city = models.CharField(default=g.city, max_length=15)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    post_id = models.IntegerField()
    post_user_id = models.IntegerField()
    let = models.CharField(max_length=30)
    long = models.CharField(max_length=30)
    date_time = models.DateTimeField(default=timezone.now)



class UserAddCar(models.Model):
    c_id = models.AutoField(primary_key=True, null=False)
    c_title = models.CharField(max_length=100)
    c_select_image = models.URLField()
    c_car_image = models.ImageField(upload_to='posts/img', null=True)
    c_car_model = models.CharField(max_length=8)
    c_self_driver = models.CharField(max_length=20)
    c_car_name = models.CharField(max_length=30)
    c_user_city = models.CharField(default=g.city, max_length=15)
    c_car_color = models.CharField(max_length=15)
    c_car_about = models.TextField()
    c_par_day_price = models.CharField(max_length=20)
    c_car_plate = models.CharField(max_length=20)
    c_post_by_user_name = models.CharField(max_length=20)
    c_post_by_user_phone = models.CharField(max_length=15)
    c_post_by_user_id = models.IntegerField()
    c_post_by_user_pic = models.URLField(default='')
    c_address = models.CharField(max_length=50)
    c_log_2 = models.CharField(max_length=30)
    c_let_1 = models.CharField(max_length=30)
    c_date_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, models.CASCADE)
