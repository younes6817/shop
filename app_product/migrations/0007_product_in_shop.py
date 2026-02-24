
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0006_remove_product_description_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_shop',
            field=models.BooleanField(default=False, verbose_name='وجود در سبد خرید'),
        ),
    ]

