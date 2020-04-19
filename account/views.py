from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserExtData, CarImages, UserAddCar
from django.contrib import auth
import os
# Create your views here.
import datetime


def login(request):
    if request.user.is_authenticated:
        return redirect(my_account)
    if request.method == 'POST':
        login_name = request.POST['user-name']
        login_pass = request.POST['user-password']
        user = auth.authenticate(username=login_name, password=login_pass)
        if user is not None:
            auth.login(request, user)
            return redirect(my_account)
        else:
            return render(request, 'account/login.html', {'error':'invalid login !'})
    return render(request, 'account/login.html')


def logout(request):
    auth.logout(request)
    return redirect(login)





def register(request):
    if request.method == 'POST':
        login_name = request.POST['user-name']
        login_pass = request.POST['user-password']
        login_phone = request.POST['user-phone']
        login_email = request.POST['user-email']
        try:
            User.objects.get(username=login_name)
            return render(request, 'account/register.html', {'error':'Username Already Exist! try: different username'})
        except User.DoesNotExist:
            user = User.objects.create_user(username=login_name, password=login_pass,)
            extdata = UserExtData(user_email=login_email, phone_no=login_phone, user=user)
            extdata.save()
            auth.login(request, user)
            return redirect(my_account)
    return render(request, 'account/register.html')





def my_account(request):
    if request.user.is_authenticated:
        user_info = UserExtData.objects.filter(user=request.user)
        Car_post = UserAddCar.objects.filter(user=request.user)
        return render(request, 'account/my_account.html', {'info':user_info, 'Car_post':Car_post})
    else:
        return redirect(login)




def add_car(request):
    if request.user.is_authenticated:
        # user_info = UserExtData.objects.filter(user=request.user)
        get_imgs = CarImages.objects.all()
        year = datetime.date.today().year
        year1 = range(2000, year+1)
        if request.method == "POST":
            _title = request.POST['c-title']
            _select_car = request.POST['c-car-name']
            _select_car_image = request.POST['c-select-image']
            _c_color = request.POST['c-color']
            _par_day_price = request.POST['c-par-day-price']
            _car_model = request.POST['c-model']
            _c_address = request.POST['c-address']
            _c_no_plate = request.POST['c-number-plate']
            _c_self_drive = request.POST['c-self-driver']
            _c_dec = request.POST['c-dec']
            _c_let = request.POST['c-let-1']
            _c_log = request.POST['c-log-2']
            # add data on database
            _add_post = UserAddCar(user=request.user, c_title=_title, c_car_name=_select_car, c_car_color=_c_color,
                                   c_par_day_price=_par_day_price, c_car_model=_car_model, c_address=_c_address,
                                   c_car_plate=_c_no_plate, c_self_driver=_c_self_drive, c_car_about=_c_dec,
                                   c_let_1=_c_let, c_log_2=_c_log, c_select_image=_select_car_image)
            _add_post.save()

        return render(request, 'account/add_car.html', {"get_imgs":get_imgs, "years":year1})
    else:
        return redirect(login)




def view_post(request, post_id):
    if request.user.is_authenticated:
        user_info = UserExtData.objects.filter(user=request.user)
        view_post = get_object_or_404(UserAddCar, pk=post_id)
        return render(request, 'account/view_post.html', {'info':user_info, 'view_post_id':view_post})
    else:
        return redirect(login)