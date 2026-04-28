# urls.py

from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path("start/<int:product_id>/", views.start_payment, name="start_payment"),
    path("verify/", views.verify_payment, name="verify_payment"),
]