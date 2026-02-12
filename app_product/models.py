from django.db import models

class Product(models.Model):
    category = models.ForeignKey('app_category.Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    discount_percent = models.PositiveBigIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    image_uploud = models.ImageField(null=True, blank=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('app_category.Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
    @property
    def final_price(self):
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price
    
class ProductSpec(models.Model):
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    key = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.key}: {self.value} for {self.product.name}"