from django.shortcuts import render, get_object_or_404
from account.models import UserAddCar
import geocoder
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
    search_home_page = UserAddCar.objects.filter(c_title__icontains=search_car_by_name, c_user_city__icontains=search_location)
    return render(request, 'home_search.html', {'search_home_page':search_home_page})
