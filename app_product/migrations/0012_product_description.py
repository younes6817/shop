
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0011_remove_product_in_shop_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات محصول'),
        ),
    ]

