


from django.urls import path
from . import views

urlpatterns = [
    path('<int:U_id>/', views.profile),
    path('profile_image/', views.ProfileImg, name='profile_image'),
    path('profile_setting/', views.profile_settings, name='profile_settings'),
]