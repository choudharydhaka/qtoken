# Generated by Django 3.0.6 on 2020-05-09 11:05

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('liquor', '0004_auto_20200509_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 9, 23, 5, 27, 128806), verbose_name='date Updated'),
        ),
        migrations.AlterField(
            model_name='liquorstore',
            name='store_id',
            field=models.CharField(default=uuid.UUID('9d74ea25-fbcc-485f-85e1-3437bd30c1a4'), max_length=200),
        ),
        migrations.AlterField(
            model_name='liquorstore',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 9, 23, 5, 27, 178582), verbose_name='date Updated'),
        ),
        migrations.AlterField(
            model_name='storeowner',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 9, 23, 5, 27, 177606), verbose_name='date Updated'),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 9, 23, 5, 27, 178582), verbose_name='Token created'),
        ),
    ]
