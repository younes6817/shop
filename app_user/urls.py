from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.main_view, name='profile')
]
