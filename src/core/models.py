"""Models module"""

from django.db import models


# pylint: disable=[no-member, undefined-variable]

# Mapping to the database tables

class Tiles(models.Model):
    """Tiles Table"""
    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)


class Dataset(models.Model):
    """Table for the dataset"""
    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    water = models.BooleanField()
    land = models.BooleanField()
    building = models.BooleanField()


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


class CaptchaSubmissions(models.Model):
    """Submitted CAPTCHAs"""
    id = models.AutoField(primary_key=True)

    # We cannot just reference a tile as it's not yet identified, so it doesn't exist in the DB
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)

    water = models.BooleanField()
    land = models.BooleanField()
    building = models.BooleanField()

    church = models.BooleanField()
    oiltank = models.BooleanField()
