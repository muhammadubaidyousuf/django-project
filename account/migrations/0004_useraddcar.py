# Generated by Django 3.0.4 on 2020-04-13 08:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20200409_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_title', models.CharField(max_length=100)),
                ('c_car_name', models.CharField(max_length=25)),
                ('c_car_color', models.CharField(max_length=20)),
                ('c_par_day_price', models.CharField(max_length=50)),
                ('c_car_model', models.CharField(max_length=25)),
                ('c_address', models.CharField(max_length=50)),
                ('c_car_plate', models.CharField(max_length=50)),
                ('c_self_driver', models.BooleanField()),
                ('c_car_about', models.TextField(max_length=300)),
                ('c_let_1', models.CharField(max_length=150)),
                ('c_log_2', models.CharField(max_length=150)),
                ('c_select_image', models.URLField()),
                ('c_date_time', models.DateField(default=datetime.datetime(2020, 4, 13, 8, 6, 28, 983230, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
