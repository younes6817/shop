from django.urls import path, include
from . import views

app_name = "orders"

urlpatterns = [
    path('', views.order_view, name='order_view'),
]