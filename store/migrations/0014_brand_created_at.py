# Generated by Django 4.2.13 on 2024-06-13 18:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_brand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
