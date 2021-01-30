from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .sitemaps import PostSitemap, StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static
from . import views


sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('', views.home, name='home'),
    path('post/<int:p_id>/<slug:slug>/', views.post_views, name='post'),
    path('accounts/', include('accounts.urls')),
    path('profile/', include('userprofile.urls'), name='profile'),
    path('search/', views.home_search, name='search'),
    path('booking_request/', views.bookingRequest, name='booking_request'),
    path('contact/', views.contact_us, name='contact_us'),
    path('get_city_location/', views.get_city_location, name='get_city_location'),
    path('PostSave/', views.PostSave, name='PostSave'),
    path('unlike/', views.Unlike, name='unlike'),
    path('p/<slug:slug>/', views.tag_view),
    path('subscribe/', views.Subscribe, name='subscribe'),
    path('email_verify/', views.EmailVerify, name='email_verify'),
    path('tags/<slug:slug>/', views.tags, name='tags'),
    path('autofill/', views.SearchAutoFill, name='autofill'),
    path('search_filter/', views.SearchFilter, name='search_filter'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)