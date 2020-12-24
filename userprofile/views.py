from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
import os
from django.contrib.auth.models import User
from accounts.models import UserAddCar
from userprofile.models import UserInformationExt
# Create your views here.


def profile(request, U_id):
    user_info = UserInformationExt.objects.get(id=U_id)
    user_post = UserAddCar.objects.filter(userext=U_id)
    return render(request, 'profile/profile.html', {'profile':user_info, 'user_post':user_post})



def profile_settings(request):
	if request.user.is_authenticated:
		user = request.user
		info = UserInformationExt.objects.get(user=request.user)
		if request.method == 'POST':
			e_full_name = request.POST['user_name']
			e_phone_number = request.POST['phone_number']
			e_address = request.POST['address']
			info.full_name = e_full_name
			info.user_phno = e_phone_number
			info.user_location = e_address
			info.save()
			messages.success(request, "Profile Update Successfully")
	return render(request, 'accounts/profile_settings.html', {'Profile_Info':info})



def ProfileImg(request):
	if request.user.is_authenticated:
		user = request.user
		model = UserInformationExt.objects.get(user=request.user)
		if request.method == "POST":
			image = request.FILES['ProfileImage']
			model.user_profile_image = image
			model.save()
			return HttpResponse('true')
		return HttpResponse("false")

