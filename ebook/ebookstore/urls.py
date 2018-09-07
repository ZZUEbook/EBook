from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('admin', views.administrator, name='administrator'),
    path('admin_login', views.administrator_Login, name='administrator_Login'),
]