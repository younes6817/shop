from django.db import models
from app_user.models import User

class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_newsletter = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    notification_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
