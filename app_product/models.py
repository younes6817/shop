from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="نام محصول"
    )
    price = models.IntegerField(
        verbose_name="قیمت (تومان)"
    )
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="درصد تخفیف"
    )
    sold_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد فروش"
    )
    stock = models.PositiveIntegerField(
        verbose_name="موجودی"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    category = models.ForeignKey(
        'app_category.Category',
        on_delete=models.CASCADE,
        verbose_name="دسته‌بندی"
    )

    in_shop = models.BooleanField(
        default=False,
        verbose_name="وجود در سبد خرید"
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        
    
    @property
    def final_price(self):
        if self.discount_percent > 0:
            return self.price * (1 - self.discount_percent / 100)
        return self.price
    
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method to validate the model
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
    
class ProductSpec(models.Model):
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE)
    key = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.key}: {self.value} for {self.product.name}"
    
    class Meta:
        verbose_name = "مشخصات محصول"
        verbose_name_plural = "مشخصات محصولات"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)  # همچنان وجود دارد


    def save(self, *args, **kwargs):
        if not self.alt_text and self.product:
            self.alt_text = self.product.name
        super().save(*args, **kwargs)