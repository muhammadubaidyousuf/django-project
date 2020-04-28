from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from account.models import UserExtData, UserAddCar
# Create your views here.


def profie(request, U_id):
    user = User.objects.filter(id=U_id)
    user_info = get_object_or_404(UserExtData, user=U_id)
    for i in user:
        id = i.id
        profile_name = i.username
    User_post = UserAddCar.objects.filter(user=id)
    return render(request, 'profile/profile.html', {'User_post':User_post, 'profile_name':profile_name, 'user_info':user_info})
