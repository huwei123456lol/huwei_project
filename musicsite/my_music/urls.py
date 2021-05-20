from django.urls import path
from . import views
urlpatterns = [
    path(r'user/login', views.login),
    path(r'user/info', views.checkuser),
    path(r'user/register', views.myregister),
    path(r'user/check', views.register),
    path(r'user/my_music', views.my_music_list),
    path(r'user/index', views.mymusic),
    path(r'user/search', views.searchByValue),
    path(r'user/find', views.findValue),
    path(r'user/sing', views.sing),
    path(r'user/myInfo', views.myUserInfo),
    path(r'user/displayInfo', views.displayMyInfo),
    path(r'user/update', views.updateMyInfo),
    path(r'user/imgdir', views.acceptImg),
]
