from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from userprofile.models import UserInformationExt
from taggit.managers import TaggableManager
import geocoder
g = geocoder.ip('me')


class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time_snt = models.DateTimeField(default=timezone.now)
    otp = models.SmallIntegerField()


class CarsName(models.Model):
    make_by = models.CharField(max_length=30)
    def __str__(self):
        return self.make_by

class CarsModel(models.Model):
    make_by_id = models.ForeignKey(CarsName, on_delete = models.CASCADE)
    model_name = models.CharField(max_length=30)
    def __str__(self):
        return self.model_name


class EmailSubscribe(models.Model):
    sbc_email = models.CharField(max_length=70)
    date_time = models.DateTimeField(default=timezone.now)
    email_verify = models.SmallIntegerField()
    status_check = models.BooleanField(default=False)
    
    def __str__(self):
        return self.sbc_email


class SavePost(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	post_id = models.IntegerField(blank=True, null=True)
	date_time = models.DateTimeField(default=timezone.now)



class ContactUs(models.Model):
    user_name = models.CharField(max_length=30)
    user_phone = models.CharField(max_length=15)
    user_email = models.CharField(max_length=30)
    message = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name


class UserBookCar(models.Model):
    full_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    message = models.TextField()
    post_title = models.CharField(max_length=100)
    city = models.CharField(default=g.city, max_length=15)
    start_date = models.CharField(max_length=30)
    end_date = models.CharField(max_length=30)
    post_id = models.IntegerField()
    post_path = models.URLField(max_length=250, blank=True, null=True)
    booking_update = models.IntegerField(blank=True, null=True)
    status_check = models.BooleanField(default=False)
    post_user_id = models.IntegerField()
    let = models.CharField(max_length=30)
    long = models.CharField(max_length=30)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name


class UserAddCar(models.Model):
    c_id = models.AutoField(primary_key=True, null=False)
    c_title = models.CharField(max_length=70)
    c_select_image = models.ImageField(upload_to='posts/img', null=True, blank=True)
    c_car_model = models.CharField(max_length=8)
    c_self_driver = models.CharField(max_length=5)
    c_make_by = models.CharField(max_length=20, null=True, blank=True)
    c_car_name = models.CharField(max_length=30)
    c_user_city = models.CharField(max_length=15, null=True, blank=True)
    c_user_state = models.CharField(max_length=15, null=True, blank=True)
    c_car_color = models.CharField(max_length=15)
    c_car_about = models.TextField(max_length=400)
    c_par_day_price = models.IntegerField()
    c_car_plate = models.CharField(max_length=20)
    c_address = models.CharField(max_length=200)
    c_log_2 = models.CharField(max_length=30)
    c_let_1 = models.CharField(max_length=30)
    c_admin_approved = models.BooleanField(default=False)
    c_view_counter = models.IntegerField(blank=True, null=True)
    c_date_time = models.DateTimeField(default=timezone.now)
    c_slug = models.SlugField(max_length=40, null=True, blank=True)
    tags = TaggableManager()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    userext = models.ForeignKey(UserInformationExt, on_delete = models.CASCADE)

    def __str__(self):
        return self.c_title

    def get_absolute_url(self):
    	return reverse('post', args=[str(self.c_id), str(self.c_slug)])




class PostsImages(models.Model):
    post_id = models.ForeignKey(UserAddCar, on_delete = models.CASCADE)
    multi_imgs = models.FileField(upload_to='posts/multi-img', max_length=255, null=True)