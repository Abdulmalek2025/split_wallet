# Generated by Django 4.1.6 on 2023-02-22 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0008_alter_request_approved_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]
