from django.db import models
from app_product.models import Product

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    image_url = models.URLField(blank=True, null=True, verbose_name="آدرس عکس (URL)")
    image_upload = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="عکس آپلودی")
    
    link_to = models.URLField(blank=True, null=True, verbose_name="لینک خارجی")
    product_to = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="لینک به محصول"
    )
    
    position = models.PositiveIntegerField(default=0, verbose_name="موقعیت")

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()
        
        if not self.image_url and not self.image_upload:
            raise ValidationError("حداقل یکی از «آدرس عکس» یا «عکس آپلودی» را پر کنید.")
        
        if self.image_url and self.image_upload:
            raise ValidationError("فقط یکی از گزینه‌ها را انتخاب کنید.")
        
        if not self.link_to and not self.product_to:
            raise ValidationError("حداقل یکی از «لینک خارجی» یا «لینک به محصول» را پر کنید.")
        
        if self.link_to and self.product_to:
            raise ValidationError("فقط یکی از لینک‌ها را انتخاب کنید.")

    def save(self, *args, **kwargs):
        if self.image_url and self.image_url.strip().lower() == 'none':
            self.image_url = None
        elif self.image_url:
            self.image_url = self.image_url.strip()

        if self.image_upload and str(self.image_upload) == 'None':
            self.image_upload = None

        self.full_clean()
        super().save(*args, **kwargs)


    @property
    def final_link(self):
        """لینک نهایی برای استفاده در تمپلیت"""
        if self.product_to:
            from django.urls import reverse
            return reverse('product:product', args=[self.product_to.pk])
        return self.link_to
