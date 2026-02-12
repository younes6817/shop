from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField()
    link_to = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
