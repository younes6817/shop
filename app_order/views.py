from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import *

def order_view(request):
    cutoff = timezone.now() - timedelta(minutes=30)
    Order.objects.filter(status='pending', created_at__lt=cutoff).update(status='error')

    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set__product').order_by('-created_at')

    return render(request, "orders.html", {
        "orders": orders,
    })