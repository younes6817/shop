from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class Address(models.Model):
    user = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True)
    full_name = models.CharField(max_length=50)
    province = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    minimal_address = models.TextField()
    building_no = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ]
    )
    postal_code = models.PositiveBigIntegerField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="کد پستی باید 10 رقمی باشد"
            )
        ]
    )
    hidden = models.BooleanField(default=False)
