from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .email_sender import OTPEmailSender
from .middelware import auth_middleware
from userprofile.models import UserInformationExt
from .models import UserAddCar,  CarImages, UserBookCar, UserOTP, SavePost, PostsImages
from django.contrib.auth.models import auth
import random 
import re
# Create your views here.
import datetime



def login(request):
    return_url = None
    return_url = request.GET.get('return_url')
    if request.user.is_authenticated:
        return redirect(my_account)
    if request.method == 'POST':
        login_email = request.POST['user-name']
        login_pass = request.POST['user-password']
        user = auth.authenticate(username=login_email, password=login_pass)
        if user is not None:    
            auth.login(request, user)
            if return_url:
                return redirect(return_url)
            else:
                return_url = None
                return redirect(my_account)    
        elif not User.objects.filter(username=login_email).exists():
            return render(request, 'accounts/login.html', {'error':'Email DoesNotExist, Please SingUp'})

        elif not User.objects.get(username=login_email).is_active:
            otp_user = User.objects.get(username=login_email)
            request.session['session_email'] = login_email
            random_otp = random.randint(100000, 999999)
            otp_save = UserOTP.objects.create(user=otp_user, otp=random_otp)
            otp_save.save()
            print(random_otp)
            # OTPEmailSender(login_email, random_otp) 
            return redirect(email_verify)
        else:
            return render(request, 'accounts/login.html', {'error':'Login Information Not Correct'})
    return render(request, 'accounts/login.html')



def resend_otp(request):
    if request.method == "POST":
        get_user = request.session.get('session_email', default=False)
        if not get_user:
            return render(request, 'accounts/404_page.html')
        elif User.objects.filter(username=get_user).exists() and not User.objects.get(username=get_user).is_active:
            user = User.objects.get(username=get_user)
            random_otp = random.randint(100000, 999999)
            otp_save = UserOTP.objects.create(user=user, otp=random_otp)
            otp_save.save()
            print(random_otp)
            # OTPEmailSender(login_email, random_otp) 
            return JsonResponse({'status':'send'})
        else:
            return JsonResponse({'status':0})


def logout(request):
    session_city = request.session.get('user-city', default=False)
    auth.logout(request)
    request.session['user-city'] = session_city
    print(session_city)
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
                user = User.objects.create_user(username=login_email, password=login_pass, email=login_email, is_active = False)
                extdata = UserInformationExt(full_name=login_name, user_email=login_email, user_phno=login_phone, user=user, user_profile_image=None)
                extdata.save()
                request.session['session_email'] = login_email
                random_otp = random.randint(100000, 999999)
                otp1 = UserOTP.objects.create(user=user, otp=random_otp)
                otp1.save()
                print(random_otp)
                OTPEmailSender(login_email, random_otp)
                return redirect(email_verify)
    return render(request, 'accounts/register.html')


def error_404_page(request):
    return render(request, 'accounts/404_page.html')



def email_verify(request):
    get_user = request.session.get('session_email', default=False)
    if not get_user:
        return render(request, 'accounts/404_page.html', {'error':''})
    if request.method == "POST":
        get_otp = request.POST['otp']
        user_name = User.objects.get(username=get_user)
        if int(get_otp) == UserOTP.objects.filter(user=user_name).last().otp:
            user_name.is_active = True
            user_name.save()
            auth.login(request, user_name)
            return redirect(my_account)
        else:
            return render(request, 'accounts/email_verify.html', {'error':'OTP Not Match, Try Again'})
    return render(request, 'accounts/email_verify.html')




def my_account(request):
    if request.user.is_authenticated:
        Car_post = UserAddCar.objects.filter(user=request.user)
        paginator = Paginator(Car_post, 10)
        page_no = request.GET.get('page')
        paje_object = paginator.get_page(page_no)
        return render(request, 'accounts/my_account.html', {'Car_post':paje_object, 'PageItems':paje_object})
    else:
        return redirect(login)



@auth_middleware
def add_car(request):
    get_imgs = CarImages.objects.all()
    year = datetime.date.today().year
    year1 = range(2000, year+1)
    user = request.user
    if request.method == "POST":
        title = request.POST['c-title']
        select_car = request.POST['c-car-name']
        multiple_image = request.FILES.getlist('files[]')
        c_color = request.POST['c-color']
        par_day_price = request.POST['c-par-day-price']
        car_model = request.POST['c-model']
        c_address = request.POST['c-address']
        c_no_plate = request.POST['c-number-plate']
        c_self_drive = request.POST['c-self-driver']
        c_dec = request.POST['c-dec']
        c_let = request.POST['c-let-1']
        c_log = request.POST['c-log-2']
        slug = slugify(title)
        userext = UserInformationExt.objects.get(user=user)
        add_post = UserAddCar(userext=userext, user=user, c_title=title, c_car_name=select_car, c_car_color=c_color,
                               c_par_day_price=par_day_price, c_car_model=car_model, c_address=c_address,
                               c_car_plate=c_no_plate, c_self_driver=c_self_drive, c_car_about=c_dec,
                               c_let_1=c_let, c_log_2=c_log, c_slug=slug)
        # add_post.save()
        for images in multiple_image:
            fs = FileSystemStorage()
            file_path = fs.save(images.name, images)
            print(file_path)
            post_image = PostsImages(post_id=add_post, multi_imgs=file_path)
            # post_image.save()
        messages.success(request, "Car ADD Successfully")
    return render(request, 'accounts/add_car.html', {"get_imgs":get_imgs, "years":year1})



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


def booking(request):
    if request.user.is_authenticated:
        user = request.user
        status_update = UserBookCar.objects.filter(post_user_id=user.id-1).update(status_check=True)
        bookings = UserBookCar.objects.filter(post_user_id=user.id-1).order_by('-date_time')
        for_post = UserBookCar.objects.filter(post_user_id=user.id-1).values_list('post_id', flat=True)
        cars_post = UserAddCar.objects.filter(c_id__in=for_post)
        paginator = Paginator(bookings, 10)
        page_no = request.GET.get('page')
        paje_object = paginator.get_page(page_no)
        return render(request, 'accounts/booking.html', {'bookings':paje_object, 'PageItems':paje_object, 'cars_post':cars_post})
    else:
        return redirect(login)


def favorite_post(request):
    user = request.user
    save_post = SavePost.objects.filter(user=user).values_list('post_id', flat=True)
    fav_post = UserAddCar.objects.filter(c_id__in=save_post)
    paginator = Paginator(fav_post, 10)
    page_no = request.GET.get('page')
    paje_object = paginator.get_page(page_no)
    return render(request, 'accounts/favorite_post.html', {'fav_post':paje_object})

