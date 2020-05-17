"""Models module"""

from random import randint

from django.db import models

# pylint: disable=[no-member, undefined-variable]

# Mapping to the database tables

class Tiles(models.Model):
    """Tiles Table"""
    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)

    def random(self):
        """ Picks a random entry """
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


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
