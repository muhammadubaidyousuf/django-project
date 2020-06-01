from django.shortcuts import render, get_object_or_404, HttpResponse
from accounts.models import UserAddCar, UserBookCar
from django.contrib import messages
import geocoder
import re
geo = geocoder.ip('me')

def home(request):
    city = geo.city
    home_page_post = UserAddCar.objects.filter(c_user_city=city)[:7]
    return render(request, 'home.html', {'Home_page_post':home_page_post})


def post_views(request, p_id):
    home_post_by_id = get_object_or_404(UserAddCar, pk=p_id)
    return render(request, 'post.html', {'home_post_by_id':home_post_by_id})


def home_search(request):
    search_car_by_name = request.GET['search-car-name']
    search_location = request.GET['search-location']
    if len(search_car_by_name) > 50 or len(search_location) >50:
        search_home_page = []
    else:
        search_home_page = UserAddCar.objects.filter(c_title__icontains=search_car_by_name, c_user_city__icontains=search_location)
    return render(request, 'home_search.html', {'search_home_page':search_home_page})





def bookingRequest(request):
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
    post = UserBookCar(post_title=post_title, post_id=post_id, post_user_id=post_user_id,
                       full_name=full_name, phone_no=phone_no, address=address, message=msg,
                       let=let, long=long, start_date=start_date, end_date=end_date)
    try:
        post.save()
        return HttpResponse('true')
    except:
        return HttpResponse('false')

