


from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:U_id>/', views.profie),

]