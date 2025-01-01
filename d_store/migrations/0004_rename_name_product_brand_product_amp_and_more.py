# Generated by Django 5.1.4 on 2025-01-01 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_store', '0003_product_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='amp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='psi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type_oild',
            field=models.CharField(blank=True, choices=[('Sintentico', 'Sintentico'), ('Semi-sintentico', 'Semi-sintentico'), ('Mineral', 'Mineral')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='viscosity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='volts',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_parts', to='d_store.category'),
        ),
    ]