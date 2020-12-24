from .models import UserBookCar, SavePost
from userprofile.models import UserInformationExt
from taggit.models import Tag
from django.http import Http404
from django.shortcuts import HttpResponse

# def all_notification(get_response):

#     def notificaton_ware(request):
#     	print('noti')
#     	response = get_response(request)
#     	return response

#     return notificaton_ware





def Notifications(request):
	notification_count = 0
	if request.user.is_authenticated:	
		user = request.user
		notification_count = UserBookCar.objects.filter(post_user_id=user.id-1, status_check=False).count()
	return {'notification_count':notification_count}


def SessionOn(request):
	session = True
	if not request.session.get('user-city', default=False):
		session = False
	else:
		session = True
	return {'session': session}


def Profile_image(request):
	profile_img = None
	if request.user.is_authenticated:
		user = request.user
		profile_img = UserInformationExt.objects.filter(user=user)
	return {'profile_img':profile_img}



def AllTags(request):
	alltags = Tag.objects.all()
	return {'alltags':alltags}
