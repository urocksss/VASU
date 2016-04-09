from django.conf.urls import url

from . import views

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^$', views.print_history, name='print_history'),
	
]
