
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_banner', '0001_initial'),
        ('app_product', '0008_rename_image_uploud_product_image_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='product_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_product.product', verbose_name='لینک به محصول'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_upload',
            field=models.ImageField(blank=True, null=True, upload_to='banners/', verbose_name='عکس آپلودی'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='آدرس عکس (URL)'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link_to',
            field=models.URLField(blank=True, null=True, verbose_name='لینک خارجی'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='position',
            field=models.PositiveIntegerField(default=0, verbose_name='موقعیت'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان'),
        ),
    ]

