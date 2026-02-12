from django.db import models

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.code} - {self.percentage}%"
