# Generated by Django 3.2.6 on 2022-04-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0008_alter_user_activation_key_expire'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=2084, verbose_name='Фото'),
        ),
    ]