# Generated by Django 4.1.7 on 2023-04-21 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charging_stations', '0010_remove_dhmos_chargers_dhmos_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='address',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
