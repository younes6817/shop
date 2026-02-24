
import colorfield.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0012_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color_name',
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='رنگ')),
                ('color_name', models.CharField(max_length=20, verbose_name='نام رنگ')),
                ('stock', models.PositiveBigIntegerField(verbose_name='موجودی این رنگ')),
                ('is_default', models.BooleanField(default=False, verbose_name='رنگ پیشفرض')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='app_product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'رنگ محصول',
                'verbose_name_plural': 'رنگ\u200cهای محصول',
                'ordering': ['-is_default', 'color_name'],
            },
        ),
    ]

