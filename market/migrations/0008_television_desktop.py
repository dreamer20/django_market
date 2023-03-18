# Generated by Django 4.1.7 on 2023-03-17 12:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import market.validators
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_rename_order_id_order_items_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Television',
            fields=[
                ('product_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='market.product_code', to_field='product_code')),
                ('brand', models.CharField(max_length=300)),
                ('model', models.CharField(max_length=300)),
                ('product_image', models.ImageField(blank=True, upload_to='product_images/')),
                ('price', models.FloatField(validators=[market.validators.validate_price])),
                ('count', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('decription', tinymce.models.HTMLField(blank=True, default='')),
                ('refresh_rate', models.IntegerField(blank=True)),
                ('resolution', models.CharField(blank=True, max_length=300)),
                ('display_technology', models.CharField(blank=True, max_length=300)),
                ('connectivity_technology', models.CharField(blank=True, max_length=300)),
                ('product_dimensions', models.CharField(blank=True, max_length=300)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Desktop',
            fields=[
                ('product_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='market.product_code', to_field='product_code')),
                ('brand', models.CharField(max_length=300)),
                ('model', models.CharField(max_length=300)),
                ('product_image', models.ImageField(blank=True, upload_to='product_images/')),
                ('price', models.FloatField(validators=[market.validators.validate_price])),
                ('count', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('decription', tinymce.models.HTMLField(blank=True, default='')),
                ('disk_size', models.IntegerField(blank=True)),
                ('cpu', models.CharField(blank=True, max_length=300)),
                ('gpu', models.CharField(blank=True, max_length=300)),
                ('os', models.CharField(blank=True, max_length=100)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]