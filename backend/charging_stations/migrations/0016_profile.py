# Generated by Django 4.1.7 on 2023-05-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charging_stations', '0015_station_mean_updating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]