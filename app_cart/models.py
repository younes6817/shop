from django.conf import settings
from django.db import models
from app_product.models import ProductColor

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"سبد خرید {self.user.email}"

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_color = models.ForeignKey(
        ProductColor,
        on_delete=models.SET_NULL,
        related_name='cart_items',
        null=True,
        blank=True,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def total_price(self):
        return self.product.final_price * self.quantity

    @property
    def persian_total_price(self):
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        value = "{:,}".format(int(self.total_price))
        return "".join(persian_digits[int(ch)] if ch.isdigit() else ch for ch in value)
