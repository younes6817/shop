
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0009_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_upload',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]

