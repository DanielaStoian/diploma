# Generated by Django 4.1.7 on 2023-05-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charging_stations', '0016_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_check',
            field=models.DateTimeField(null=True),
        ),
    ]