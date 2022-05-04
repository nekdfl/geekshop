# Generated by Django 3.2.6 on 2022-04-27 10:27

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0005_auto_20220426_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expire',
            field=models.DateTimeField(blank=True,
                                       default=datetime.datetime(2022, 4, 30, 10, 27, 37, 432387, tzinfo=utc),
                                       null=True),
        ),
    ]