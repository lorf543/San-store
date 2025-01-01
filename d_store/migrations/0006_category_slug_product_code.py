# Generated by Django 5.1.4 on 2025-01-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_store', '0005_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
