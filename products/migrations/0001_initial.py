# Generated by Django 3.0.8 on 2020-07-12 10:30

import django.core.validators
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3, 'Invalid product name'), django.core.validators.MaxLengthValidator(55, 'Invalid product name')])),
                ('value', models.FloatField(validators=[products.models.validate_value])),
                ('discount_value', models.FloatField()),
                ('stock', models.IntegerField(validators=[products.models.validate_stock])),
            ],
        ),
    ]
