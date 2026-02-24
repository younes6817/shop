
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0013_remove_product_color_remove_product_color_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspec',
            name='key',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='کلید'),
        ),
        migrations.AlterField(
            model_name='productspec',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='app_product.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productspec',
            name='value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='مقدار'),
        ),
    ]

