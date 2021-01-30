from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.UserAddCar)
class UserPosts(admin.ModelAdmin):
	list_display = ['c_id', 'c_title', 'user', 'c_date_time', 'c_user_city', 'c_par_day_price', 'c_car_plate', 'c_address', 'c_admin_approved']
	list_display_links = ('c_title',)
	list_editable = ('c_admin_approved',)
	search_fields = ('user', 'c_title',)
	list_filter = ('c_date_time',)

admin.site.register(models.ContactUs)
admin.site.register(models.SavePost)

@admin.register(models.EmailSubscribe)
class EmailSubscribe(admin.ModelAdmin):
	list_display = ['id', 'sbc_email', 'date_time', 'status_check']
	list_display_links = ('sbc_email',)
	list_editable = ('status_check',)
	search_fields = ('sbc_email',)
	ordering = ['sbc_email']
	list_filter = ('date_time',)


@admin.register(models.CarsName)
class CarsName(admin.ModelAdmin):
	list_display = ['id', 'make_by']

@admin.register(models.CarsModel)
class CarsModel(admin.ModelAdmin):
	list_display = ['id', 'make_by_id', 'model_name']
	list_display_links = ('model_name',)


@admin.register(models.UserBookCar)
class AllBookings(admin.ModelAdmin):
	list_display=['full_name', 'phone_no', 'address', 
	'post_title', 'city', 'start_date', 'end_date', 'status_check', 'date_time']

@admin.register(models.PostsImages)
class PostsImages(admin.ModelAdmin):
	list_display=['id', 'multi_imgs', 'post_id']

admin.site.site_header = 'BUKINOW'