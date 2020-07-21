# Generated by Django 2.1.1 on 2020-07-21 21:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200721_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(3, 'Invalid category description'), django.core.validators.MaxLengthValidator(250, 'Invalid category description')]),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3, 'Invalid category name'), django.core.validators.MaxLengthValidator(55, 'Invalid category name')]),
        ),
    ]
