
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('image_upload', models.ImageField(blank=True, null=True, upload_to='banners/')),
                ('link_to', models.URLField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]

