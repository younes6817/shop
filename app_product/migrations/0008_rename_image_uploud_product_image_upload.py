
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0007_product_in_shop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_uploud',
            new_name='image_upload',
        ),
    ]

