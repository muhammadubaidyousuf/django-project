from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from userprofile.models import UserInformationExt
from .models import UserAddCar,  CarImages, UserBookCar
from django.contrib.auth.models import auth
import re
# Create your views here.
import datetime


def login(request):
    if request.user.is_authenticated:
        return redirect(my_account)
    if request.method == 'POST':
        login_email = request.POST['user-name']
        login_pass = request.POST['user-password']
        user = auth.authenticate(username=login_email, password=login_pass)
        if user is not None:
            auth.login(request, user)
            return redirect(my_account)
        else:
            return render(request, 'accounts/login.html', {'error':'invalid login !'})
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect(login)





def register(request):
    if request.user.is_authenticated:
        return redirect(login)
    if request.method == 'POST':
        login_name = request.POST['user-name']
        login_pass = request.POST['user-password']
        login_phone = request.POST['user-phone']
        login_email = request.POST['user-email']
        if login_name == "" and login_pass == "" and login_phone == "" and login_email == "" :
            return render(request, 'accounts/register.html', {'error': 'Fill All Field'})
        elif len(login_phone) <= 15 and not re.search("[0][3]\d{9}(?!\d)", login_phone):
            return render(request, 'accounts/register.html', {'error':'Phone Number Not Valid'})
        else:
            try:
                user = User.objects.get(username=login_email)
                return render(request, 'accounts/register.html', {'error':'Email Already Exist! try: different Email'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=login_email, password=login_pass, email=login_email)
                extdata = UserInformationExt(full_name=login_name, user_email=login_email, user_phno=login_phone, user=user)
                extdata.save()
                auth.login(request, user)
                return redirect(my_account)
    else:
        return render(request, 'accounts/register.html')





def my_account(request):
    if request.user.is_authenticated:
        Car_post = UserAddCar.objects.filter(user=request.user)
        for car in Car_post:
            car_id = car.c_id
            if car_id != 0:
                return render(request, 'accounts/my_account.html', {'Car_post':Car_post})
        else:
            return render(request, 'accounts/my_account.html', {'error': 'No Post Available'})
    else:
        return redirect(login)




def add_car(request):
    if request.user.is_authenticated:
        get_imgs = CarImages.objects.all()
        year = datetime.date.today().year
        year1 = range(2000, year+1)
        if request.method == "POST":
            _title = request.POST['c-title']
            _select_car = request.POST['c-car-name']
            _select_car_image = request.FILES['c-select-image']
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
            info = UserInformationExt.objects.get(user=request.user)
            _add_post = UserAddCar(c_post_by_user_name=info.full_name, c_post_by_user_phone=info.user_phno, user=request.user,
                                   c_title=_title, c_car_name=_select_car, c_car_color=_c_color,
                                   c_par_day_price=_par_day_price, c_car_model=_car_model, c_address=_c_address,
                                   c_car_plate=_c_no_plate, c_self_driver=_c_self_drive, c_car_about=_c_dec,
                                   c_let_1=_c_let, c_log_2=_c_log, c_select_image=_select_car_image,
                                   c_post_by_user_id=info.id, c_post_by_user_pic=info.user_profile_image)
            _add_post.save()
            messages.success(request, "Car ADD Successfully")
        return render(request, 'accounts/add_car.html', {"get_imgs":get_imgs, "years":year1})
    else:
        return redirect(login)


def post_edit(request, p_id):
    if request.user.is_authenticated:
        edit_imgs = CarImages.objects.all()
        year = datetime.date.today().year
        edit_year = range(2000, year+1)

        info = UserInformationExt.objects.filter(user=request.user)
        edit_post = get_object_or_404(UserAddCar, c_id=p_id)
        if request.method == "POST":
            e_title = request.POST['c-title']
            e_select_car = request.POST['c-car-name']
            e_select_car_image = request.FILES['c-select-image']
            e_c_color = request.POST['c-color']
            e_par_day_price = request.POST['c-par-day-price']
            e_car_model = request.POST['c-model']
            e_c_address = request.POST['c-address']
            e_c_no_plate = request.POST['c-number-plate']
            e_c_self_drive = request.POST['c-self-driver']
            e_c_dec = request.POST['c-dec']

            # edit database part
            edit = UserAddCar.objects.get(c_id=p_id)
            edit.c_title = e_title
            edit.c_select_car = e_select_car
            edit.c_select_image = e_select_car_image
            edit.c_car_color = e_c_color
            edit.c_par_day_price = e_par_day_price
            edit.c_car_model = e_car_model
            edit.c_address = e_c_address
            edit.c_car_plate = e_c_no_plate
            edit.c_self_driver = e_c_self_drive
            edit.c_car_about = e_c_dec
            edit.save()
            messages.error(request, "Post Update successfully.")
        return render(request, 'accounts/post_edit.html', {'edit_post':edit_post, 'edit_img':edit_imgs, 'edit_year':edit_year})
    else:
        return redirect(login)



def post_delete(request, d_id):
    if request.user.is_authenticated:
        delete_post = UserAddCar.objects.filter(c_id=d_id)
        messages.warning(request, "Do You Want To Delete This Post Say Yes Or No")
        delete_post.delete()
        return redirect(my_account)
    else:
        return redirect(login)




def profile_settings(request):
    if request.user.is_authenticated:
        profile_info = UserInformationExt.objects.get(user=request.user)
        if request.method == 'POST':
            e_image = request.FILES['profile_image']
            e_full_name = request.POST['user_name']
            e_phone_number = request.POST['phone_number']
            e_address = request.POST['address']
            profile_update = UserInformationExt.objects.get(user=request.user)
            profile_update.user_profile_image = e_image
            profile_update.full_name = e_full_name
            profile_update.user_phno = e_phone_number
            profile_update.user_location = e_address
            profile_update.save()
            messages.success(request, "Profile Update Successfully")
        return render(request, 'accounts/profile_settings.html', {'Profile_Info':profile_info})
    else:
        return redirect(login)


def booking(request):
    if request.user.is_authenticated:
        user = UserInformationExt.objects.get(user=request.user)
        bookings = UserBookCar.objects.filter(post_user_id=user.id).order_by('-date_time')
        return render(request, 'accounts/booking.html', {'bookings':bookings})
    else:
        return redirect(login)


