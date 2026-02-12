from django.db import models

class Cart(models.Model):
    user = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username} - Created at {self.created_at}"

class CartItem(models.Model):
    cart = models.ForeignKey('app_cart.Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_color = models.CharField(max_length=50, blank=True, null=True)
    selected_size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"

    
