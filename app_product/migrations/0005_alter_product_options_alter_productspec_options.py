
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0004_product_created_at_product_sold_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterModelOptions(
            name='productspec',
            options={'verbose_name': 'مشخصات محصول', 'verbose_name_plural': 'مشخصات محصولات'},
        ),
    ]

