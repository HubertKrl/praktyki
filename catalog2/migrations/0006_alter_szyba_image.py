# Generated by Django 5.1.7 on 2025-04-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog2', '0005_szyba_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='szyba',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
