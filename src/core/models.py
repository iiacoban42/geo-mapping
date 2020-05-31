"""Models module"""

from django.db import models


# pylint: disable=[no-member, undefined-variable, too-few-public-methods, too-many-instance-attributes]

# Mapping to the database tables
class CaptchaSubmissions(models.Model):
    """Submitted CAPTCHAs"""

    class Meta:
        """Meta CaptchaSubmissions"""
        app_label = 'core'

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
    objects = models.Manager()


class Dataset(models.Model):
    """Table for the dataset"""

    class Meta:
        """Meta Dataset"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    water = models.BooleanField()
    land = models.BooleanField()
    building = models.BooleanField()
    objects = models.Manager()


class Tiles(models.Model):
    """Tiles Table"""

    class Meta:
        """Meta Tiles"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    objects = models.Manager()


class Objects(models.Model):
    """Objects Table"""

    class Meta:
        """Meta Object"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Tiles, on_delete=models.CASCADE)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()
    objects = models.Manager()


class Characteristics(models.Model):
    """Characteristics Table"""

    class Meta:
        """Meta Characteristics"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Tiles, on_delete=models.CASCADE)
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
    objects = models.Manager()

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
    objects = models.Manager()


class ConfirmedCaptchas(models.Model):
    """Confirmed CAPTCHAs"""
    id = models.AutoField(primary_key=True)

    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)

    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()

    church_prediction = models.IntegerField()
    oiltank_prediction = models.IntegerField()
    objects = models.Manager()

