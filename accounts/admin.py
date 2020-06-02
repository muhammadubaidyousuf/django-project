from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.UserAddCar)
admin.site.register(models.CarImages)
admin.site.register(models.UserBookCar)
admin.site.register(models.ContactUs)

admin.site.site_header = 'BUKINOW'