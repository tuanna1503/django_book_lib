# Generated by Django 2.2.2 on 2019-06-21 03:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20190620_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='returns',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rentalbook',
            name='rental_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 6, 21, 3, 41, 24, 996279, tzinfo=utc)),
        ),
    ]