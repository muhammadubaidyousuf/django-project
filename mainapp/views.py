from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from accounts.models import UserAddCar, UserBookCar, ContactUs, SavePost, EmailSubscribe, PostsImages
from userprofile.models import UserInformationExt
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
import geocoder
import re
import random
geo = geocoder.ip('me')

def get_city_location(request):
    if request.method == "POST":
        user_city = request.POST['city']
        request.session['user-city'] = user_city
        return HttpResponse("session_save")


def home(request):

    city = request.session.get('user-city', default=False)
    home_page_post = UserAddCar.objects.filter(c_user_city=city)[:6]
    return render(request, 'home.html', {'Home_page_post':home_page_post})



def post_views(request, p_id, slug):
    if request.user.is_authenticated:
        user = request.user
        LikePost = SavePost.objects.filter(user=user, post_id=p_id).exists()
        home_post_by_id = get_object_or_404(UserAddCar, pk=p_id, c_slug=slug)
        images = PostsImages.objects.filter(post_id_id=home_post_by_id)
        return render(request, 'post.html', {'home_post_by_id':home_post_by_id, 'likepost':LikePost, 'images':images})  
    else:
        home_post_by_id = get_object_or_404(UserAddCar, pk=p_id, c_slug=slug)
        images = PostsImages.objects.filter(post_id_id=home_post_by_id)
        return render(request, 'post.html', {'home_post_by_id':home_post_by_id, 'images':images})  


def tags(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post = UserAddCar.objects.filter(tags=tag)
    return render(request, 'tags.html', {'post':post}) 

def tag_view(request, slug):
    slug = slug
    if "-" in slug:
        slug = slug.replace("-", " ")
    save_post = None
    if request.user.is_authenticated:
        user = request.user
        ids = UserAddCar.objects.filter(Q(c_title__icontains=slug)|Q(c_car_about__icontains=slug)|Q(c_car_model__icontains=slug)|Q(c_make_by__icontains=slug)).values_list('c_id', flat=True)
        save_post = SavePost.objects.filter(user=user, post_id__in=ids).values_list('post_id', flat=True)
    Posts = UserAddCar.objects.filter(Q(c_title__icontains=slug)|Q(c_car_about__icontains=slug)|Q(c_car_model__icontains=slug)|Q(c_make_by__icontains=slug))    
    paginator = Paginator(Posts, 10)
    page_no = request.GET.get('page')
    paje_object = paginator.get_page(page_no)
    context = {
    'tags':paje_object,
     'slug':slug,
     'PageItems':paje_object,
     'save_post':save_post
    }
    return render(request,'tag_view.html', context)

@csrf_exempt
def Unlike(request):
    if request.method == "POST":
        user = request.user
        unlike_id = request.POST.get('unlike_id')
        unlike = SavePost.objects.get(user=user, post_id__in=unlike_id)
        unlike.delete()
        return HttpResponse("Unlike")
    else:
        return HttpResponse("error")


@csrf_exempt
def PostSave(request):
    if not request.user.is_authenticated:
        return HttpResponse("not_login")
    if request.method == "POST":
        user = request.user
        post_id = request.POST['post_id']
        p = SavePost.objects.filter(user=user, post_id=post_id).exists()
        if not p:
            save_post = SavePost(user=user, post_id=post_id)
            save_post.save()
            return HttpResponse("PostSave")
        else:
            return HttpResponse("PostExists")


def home_search(request):
    search_car_by_name = request.GET.get('query')
    search_location = request.session.get('user-city')
    save_post = None
    if request.user.is_authenticated:
        user = request.user
        ids = UserAddCar.objects.filter(c_title__icontains=search_car_by_name, c_user_city__icontains=search_location).order_by('c_id').values_list('c_id', flat=True)
        save_post = SavePost.objects.filter(user=user, post_id__in=ids).values_list('post_id', flat=True)
    if 'term' in request.GET:
        get_term = request.GET.get('term').lower()
        qs = UserAddCar.objects.filter(Q(c_title__icontains=get_term)|Q(c_make_by__icontains=get_term)|Q(c_car_about__icontains=get_term)|Q(c_car_model__icontains=get_term)|Q(c_car_name__icontains=get_term))
        titles = list()
        for post_title in qs:
            titles.append(post_title.c_title)
        return JsonResponse(titles, safe=False)
    else:    
        if search_location == "" and search_car_by_name == "":
            search_home_page = []
        else:
            search_home_page = UserAddCar.objects.filter(c_title__icontains=search_car_by_name, c_user_city__icontains=search_location).order_by('c_id')
            paginator = Paginator(search_home_page, 10)
            page_no = request.GET.get('page')
            paje_object = paginator.get_page(page_no)
    return render(request, 'home_search.html', {'search_home_page':paje_object, 'loc_query': search_location, 'query_shr':search_car_by_name, 'save_post':save_post})




def bookingRequest(request):
    if request.method == "GET":
        post_title = request.GET['post_title']
        post_id = request.GET['post_id']
        post_user_id = request.GET['post_user_id']
        full_name = request.GET['full_name']
        phone_no = request.GET['phone_no']
        address = request.GET['address']
        msg = request.GET['messages']
        let = request.GET['let_1']
        long = request.GET['long_1']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        email = UserInformationExt.objects.get(id=post_user_id)
        send_email = email.user_email
        full_path = request.GET.get('post_path')
        print(full_path)
        if post_title != "" and full_name != "" and phone_no != "" and address != "" and msg != "":
            post = UserBookCar(post_title=post_title, post_id=post_id, post_user_id=post_user_id,
                               full_name=full_name, phone_no=phone_no, address=address, message=msg,
                               let=let, long=long, start_date=start_date, post_path=full_path, end_date=end_date, booking_update=+1)
            try:
                post.save()
                send_mail(
                    'New Booking - Bukinow',
                     msg,
                    'ubaidahmedmeo@gmail.com',
                    ['ubaidahmedmeo@gmail.com'],
                    fail_silently=False,)
                return HttpResponse('true')
            except:
                return HttpResponse('false')
        else:
            return HttpResponse('empty')



def contact_us(request):
    if request.method == 'POST':
        user_name = request.POST['user-name']
        user_email = request.POST['user-email']
        user_phone = request.POST['user-phone']
        user_msg = request.POST['user-msg']
        contact = ContactUs(user_name=user_name, user_email=user_email, user_phone=user_phone, message=user_msg)
        contact.save()
        return render(request, 'contact-us.html', {'error':'Message Send Successfully'})
    return render(request, 'contact-us.html')



def Subscribe(request):
    if request.method == "POST":
        email = request.POST['newsletter']
        random_no = random.randint(100000, 999999)
        email_save = EmailSubscribe(sbc_email=email, email_verify=random_no)
        email_save.save()
        message = f"{email},\n Your OTP is {request.META['HTTP_HOST']}/email_verify/?email={email}&subscribe={random_no}\nThanks"
        print(message)
        send_mail(
            "Email Verify OTP Is Ready - BUKINOW",
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False)

        return HttpResponse("Email save")


def EmailVerify(request):
    if request.method == "GET":
        verify_url = None 
        email_verify_url = request.GET.get('email')
        otp_verify_url = request.GET.get('subscribe')
        print(email_verify_url)
        print(otp_verify_url)
        if EmailSubscribe.objects.filter(sbc_email=email_verify_url).exists() and EmailSubscribe.objects.filter(email_verify=otp_verify_url).last():
            status = EmailSubscribe.objects.get(sbc_email=email_verify_url)
            status.status_check = True
            status.save()
            if status.status_check == True:
                return redirect("home")
            return HttpResponse("False.........")
        else:
            return HttpResponse("False")
    return redirect("home")





