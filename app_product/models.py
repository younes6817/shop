from django.db import models
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات محصول")
    price = models.IntegerField(verbose_name="قیمت (تومان)")
    discount_percent = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True, verbose_name="درصد تخفیف"
    )
    sold_count = models.PositiveIntegerField(default=0, verbose_name="تعداد فروش")
    stock = models.PositiveIntegerField(verbose_name="موجودی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    category = models.ForeignKey(
        'app_category.Category', on_delete=models.CASCADE, verbose_name="دسته‌بندی"
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
    
    # ✅ متد کمکی تبدیل عدد به فارسی (این رو اضافه کن!)
    def _to_persian_num(self, num):
        """تبدیل عدد انگلیسی به فارسی"""
        if num is None:
            return ''
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        return ''.join(persian_digits[int(d)] if d.isdigit() else d for d in str(num))
    
    @property
    def final_price(self):
        if self.discount_percent and self.discount_percent > 0:
            return int(self.price * (1 - self.discount_percent / 100))
        return self.price
    
    @property
    def persian_price(self):
        """قیمت اصلی به فارسی با جداکننده هزارگان"""
        return self._to_persian_num('{:,}'.format(int(self.price)))
    
    @property
    def persian_final_price(self):
        """قیمت نهایی (با تخفیف) به فارسی با جداکننده هزارگان"""
        return self._to_persian_num('{:,}'.format(int(self.final_price)))
    
    @property
    def has_colors(self):
        return self.colors.exists()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE, verbose_name="محصول")
    color = ColorField(verbose_name="رنگ")
    color_name = models.CharField(max_length=20, verbose_name="نام رنگ")
    stock = models.PositiveBigIntegerField(verbose_name="موجودی این رنگ")
    is_default = models.BooleanField(default=False, verbose_name="رنگ پیشفرض")

    class Meta:
        verbose_name = "رنگ محصول"
        verbose_name_plural = "رنگ‌های محصول"
        ordering = ['-is_default', 'color_name']

    def __str__(self):
        return f"{self.color_name} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            ProductColor.objects.filter(
                product=self.product,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
    
class ProductSpec(models.Model):
    product = models.ForeignKey('app_product.Product', on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')
    key = models.CharField(max_length=50, blank=True, null=True, verbose_name="کلید")
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name="مقدار")


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