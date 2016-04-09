from django.conf.urls import url

from feemgmt.loginfiles import LoginRequest, LogoutRequest
from . import views

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginRequest),
    url(r'^logout/$', LogoutRequest),
    url(r'^print_history/$', views.print_history, name='print_history'),
    url(r'^pay_fee/$', views.print_history, name='print_history'),

]
