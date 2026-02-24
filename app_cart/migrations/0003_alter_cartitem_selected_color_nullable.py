
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_cart", "0002_remove_cartitem_selected_size_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="selected_color",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart_items",
                to="app_product.productcolor",
            ),
        ),
    ]

