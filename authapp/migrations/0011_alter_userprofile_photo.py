# Generated by Django 3.2.6 on 2022-04-28 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0010_alter_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.CharField(blank=True, max_length=2084, null=True, verbose_name='Фото'),
        ),
    ]
