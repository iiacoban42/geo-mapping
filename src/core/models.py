"""Models module"""
from django.db import models


# Create your models here.
class Tiles(models.Model):
    """Tiles Table"""
    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)


class Objects(models.Model):
    """Objects Table"""
    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Tiles, on_delete=models.CASCADE)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()


class Characteristics(models.Model):
    """Characteristics Table"""
    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Tiles, on_delete=models.CASCADE)
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
