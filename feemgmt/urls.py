from django.conf.urls import url

from feemgmt.loginfiles import LoginRequest, LogoutRequest
from feemgmt.views import print_history, make_payment, TransactionComplete

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginRequest),
    url(r'^logout/$', LogoutRequest),
    url(r'^print_history/$', print_history, name='print_history'),
    url(r'^pay_fee/$', make_payment, name='pay_fees'),
    url(r'^paymentfinishredirect/$', TransactionComplete, name='payment complete'),

]
