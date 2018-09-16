from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('adminLogin', views.adminLogin, name='administrator_Login'),
    path('getbook', views.getbook, name='getbook'),
    path('getNotice', views.getNotice, name='getNotice'),
    path('getRankList',views.getRankList,name='getRankList'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('newBook/', views.newBook, name="newBook"),
    path('book_detail/', views.book_detail, name="book_detail"),
    path('admin', views.admin, name="admin"),
    path('addBook/', views.addBook, name="addBook"),
    path('base/', views.base, name="base"),
    path('test/', views.test, name="test"),
    path('UserManage/', views.UserManage, name="UserManage"),
    path('OrderManage/', views.OrderManage, name="OrderManage"),
    path('NoticeManage/', views.NoticeManage, name="NotiveMange"),
    path('AccountManage/', views.AccountManage, name="AccountManage"),
    path('ConmentManage/', views.ConmentManage, name="Commentmange"),
]
