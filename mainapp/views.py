from django.shortcuts import render, get_object_or_404
from accounts.models import UserAddCar, UserBookCar
import geocoder
geo = geocoder.ip('me')

def home(request):
    city = geo.city
    home_page_post = UserAddCar.objects.filter(c_user_city=city)[:7]
    return render(request, 'home.html', {'Home_page_post':home_page_post})


def post_views(request, p_id):
    home_post_by_id = get_object_or_404(UserAddCar, pk=p_id)

    if request.method == 'POST':
        post_title = request.POST['post-title']
        post_id = request.POST['post-id']
        post_user_id = request.POST['post-user-id']
        full_name = request.POST['full-name']
        phone_no = request.POST['phone-no']
        address = request.POST['address']
        message = request.POST['massage']
        let = request.POST['let']
        long = request.POST['long']
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        post = UserBookCar(post_title=post_title, post_id=post_id, post_user_id=post_user_id,
                           full_name=full_name, phone_no=phone_no, address=address, message=message,
                           let=let, long=long, start_date=start_date, end_date=end_date)
        post.save()

    return render(request, 'post.html', {'home_post_by_id':home_post_by_id})


def home_search(request):
    search_car_by_name = request.GET['search-car-name']
    search_location = request.GET['search-location']
    if len(search_car_by_name) > 50 or len(search_location) >50:
        search_home_page = []
    else:
        search_home_page = UserAddCar.objects.filter(c_title__icontains=search_car_by_name, c_user_city__icontains=search_location)
    return render(request, 'home_search.html', {'search_home_page':search_home_page})


