# Generated by Django 4.1.6 on 2023-02-14 18:09

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_wallet_emergency_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='share_percentage',
            field=models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
