# Generated by Django 4.2.13 on 2024-06-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_brand_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
