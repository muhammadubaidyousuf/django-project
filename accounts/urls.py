
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.my_account, name='my_account'),
    path('register/', views.register, name='register'),
    path('add-car/', views.add_car, name='add_car'),
    path('profile_setting/', views.profile_settings, name='profile_settings'),
    path('my-account/post-delete/<int:d_id>/', views.post_delete),
    path('my-account/post-edit/<int:p_id>/', views.post_edit, name='post_edit'),
    path('booking/', views.booking, name='booking'),




    # for password only change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    # after password change move on this page
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # now we start is user password forgot first we will ask for user email that email user provide in register time

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),

    # when user gevin his email we will send an email on user email account, in email we will send user id and token
    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    # user received an email in confirmation link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),


    # when user fill form new password and confirm password
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]
