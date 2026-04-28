from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    path('', views.addresses_view, name='address')
]