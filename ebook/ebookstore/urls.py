from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('admin', views.administrator, name='administrator'),
    path('admin_login', views.administrator_Login, name='administrator_Login'),
    path('getbook', views.getbook, name='getbook'),
    path('getNotice', views.getNotice, name='getNotice'),
    path('getRankList',views.getRankList,name='getRankList'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('admin-login/', views.adminLogin, name='adminLogin'),
]