from django.db import models

class Order(models.Model):
    user = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    total_price = models.IntegerField
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey('app_order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_buy = models.IntegerField
    selected_color = models.CharField(max_length=50, blank=True, null=True)
    selected_size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"