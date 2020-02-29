from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
]
