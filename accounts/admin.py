from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.UserAddCar)
admin.site.register(models.CarImages)
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




@admin.register(models.UserBookCar)
class AllBookings(admin.ModelAdmin):
	list_display=['full_name', 'phone_no', 'address', 
	'post_title', 'city', 'start_date', 'end_date', 'status_check', 'date_time']

@admin.register(models.PostsImages)
class PostsImages(admin.ModelAdmin):
	list_display=['id', 'multi_imgs', 'post_id']

admin.site.site_header = 'BUKINOW'