from django.db import models
from app_product.models import ProductColor
from shop.settings import base as settings
from app_address.models import Address

class Order(models.Model):
    user = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    total_price = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=settings.STATUS_ORDER_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def status_badge_classes(self):
        color_map = {
            'pending': 'bg-yellow-100/70 text-yellow-800',
            'paid': 'bg-green-100/70 text-green-800',
            'error': 'bg-red-100/70 text-red-800',
            'error_pay': 'bg-red-100/70 text-red-800',
            'error_ship': 'bg-red-200/70 text-red-800',
            'shipped': 'bg-green-200/70 text-green-800',
            'delivered': 'bg-gray-100/70 text-gray-800',
        }
        return color_map.get(self.status, 'bg-gray-200 text-gray-800')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey('app_order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_buy = models.IntegerField()
    selected_color = models.ForeignKey(
        ProductColor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    selected_size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"


