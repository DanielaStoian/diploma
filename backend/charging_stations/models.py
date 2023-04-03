from django.db import models

class Station(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    type = models.CharField(max_length=500,null=True)
    origin = models.CharField(max_length=50)
    dhmos = models.CharField(max_length=50,null=True)
    category = models.CharField(max_length=50,null=True)
