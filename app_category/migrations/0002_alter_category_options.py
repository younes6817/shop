
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_category', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته\u200cبندی', 'verbose_name_plural': 'دسته\u200cبندی\u200cها'},
        ),
    ]

