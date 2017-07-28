from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^homePage$',views.homePage),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^addFriend/(?P<id>\d+)$',views.addFriend),
    url(r'^removeFriend/(?P<id>\d+)$',views.removeFriend),
    url(r'^profilePage/(?P<id>\d+)$',views.profilePage),
]
