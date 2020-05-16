from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.models import User
from accounts.models import UserAddCar
from userprofile.models import UserInformationExt
# Create your views here.


def profile(request, U_id):
    user_info = get_object_or_404(UserInformationExt, id=U_id)
    user_post = UserAddCar.objects.filter(c_post_by_user_id=U_id)

    return render(request, 'profile/profile.html', {'profile':user_info, 'user_post':user_post})
