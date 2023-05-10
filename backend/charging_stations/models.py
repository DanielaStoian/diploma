from django.db import models

class Station(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    type = models.CharField(max_length=500,null=True)
    origin = models.CharField(max_length=50)
    mean = models.CharField(max_length=200,null=True)
    mean_updating = models.CharField(max_length=200,null=True)
    chargers_num = models.CharField(max_length=50,null=True)
    dhmos = models.ForeignKey("Dhmos", on_delete=models.CASCADE)
    # class Meta:
    #     unique_together = ('lat', 'long',)
class Dhmos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50,null=True)
    category_name = models.CharField(max_length=200,null=True)