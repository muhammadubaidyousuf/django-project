


from django.urls import path
from . import views

urlpatterns = [
    path('<int:U_id>/', views.profile),
]