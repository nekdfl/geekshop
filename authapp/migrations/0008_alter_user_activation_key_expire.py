# Generated by Django 3.2.6 on 2022-04-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0007_auto_20220427_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expire',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
