
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0003_product_discount_percent_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

