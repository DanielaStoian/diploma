# Generated by Django 4.1.7 on 2023-04-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charging_stations', '0007_station_mean'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dhmos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=50, null=True)),
                ('chargers', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='chargers',
            field=models.CharField(max_length=200, null=True),
        ),
    ]