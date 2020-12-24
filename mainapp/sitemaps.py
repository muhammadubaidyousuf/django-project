from django.contrib.sitemaps import Sitemap
from accounts.models import UserAddCar
from django.urls import reverse 

class PostSitemap(Sitemap):
	def items(self):
		return UserAddCar.objects.all()


class StaticViewSitemap(Sitemap):
	
	def items(self):
		return ['contact_us', 'home']

	def location(self, item):
		return reverse(item)