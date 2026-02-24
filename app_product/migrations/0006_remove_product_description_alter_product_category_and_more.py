
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_category', '0002_alter_category_options'),
        ('app_product', '0005_alter_product_options_alter_productspec_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_category.category', verbose_name='دسته\u200cبندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_uploud',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='عکس آپلودی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='آدرس عکس (URL)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='نام محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='قیمت (تومان)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold_count',
            field=models.PositiveIntegerField(default=0, verbose_name='تعداد فروش'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='موجودی'),
        ),
    ]

