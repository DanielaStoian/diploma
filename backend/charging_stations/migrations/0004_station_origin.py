# Generated by Django 4.1.7 on 2023-03-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charging_stations', '0003_alter_station_address_alter_station_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='origin',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
