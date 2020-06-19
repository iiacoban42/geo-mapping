"""Models module"""

from django.db import models


# pylint: disable=[no-member, undefined-variable, too-few-public-methods, too-many-instance-attributes, invalid-name]

# Mapping to the database tables

# CAPTCHA tables ################################################

class Tiles(models.Model):
    """Tiles Table used to verify CAPTCHA user input"""

    class Meta:
        """Meta Tiles"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    objects = models.Manager()


class Objects(models.Model):
    """Objects Table used to verify CAPTCHA user input"""

    class Meta:
        """Meta Object"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Tiles, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()
    objects = models.Manager()


class Characteristics(models.Model):
    """Characteristics Table used to verify CAPTCHA user input"""

    class Meta:
        """Meta Characteristics"""
        app_label = 'core'

    tiles_id = models.OneToOneField(
        Tiles,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
    objects = models.Manager()


class Captcha_Tiles(models.Model):
    """CAPTCHAs tiles"""

    class Meta:
        """Meta ConfirmedCaptchas Tiles"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    uuid = models.CharField(max_length=32, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)
    objects = models.Manager()


class Captcha_Characteristics(models.Model):
    """Characteristics Table for CAPTCHAs"""

    class Meta:
        """Meta Characteristics CAPTCHA"""
        app_label = 'core'

    tiles_id = models.OneToOneField(
        Captcha_Tiles,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
    objects = models.Manager()


class Captcha_Objects(models.Model):
    """Objects Table for CPATHCAs"""

    class Meta:
        """Meta Object"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Captcha_Tiles, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()
    objects = models.Manager()


class Confirmed_Captcha_Tiles(models.Model):
    """Confirmed CAPTCHAs tiles"""

    class Meta:
        """Meta ConfirmedCaptchas Tiles"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    objects = models.Manager()


class Confirmed_Captcha_Characteristics(models.Model):
    """Characteristics Table for confirmed CAPTCHAs"""

    class Meta:
        """Meta Characteristics CAPTCHA"""
        app_label = 'core'

    tiles_id = models.OneToOneField(
        Confirmed_Captcha_Tiles,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
    objects = models.Manager()


class Confimed_Captcha_Objects(models.Model):
    """Objects Table for confirmed CPATHCAs"""

    class Meta:
        """Meta Object"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(Confirmed_Captcha_Tiles, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()
    objects = models.Manager()


# AI tables ###############################################

class AI_Tiles(models.Model):
    """Tiles classified by the AI"""

    class Meta:
        """Meta AI Tiles"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)

    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    objects = models.Manager()


class AI_Characteristics(models.Model):
    """Characteristics Table for AI tiles"""

    class Meta:
        """Meta Characteristics AI tiles"""
        app_label = 'core'

    tiles_id = models.OneToOneField(
        AI_Tiles,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    water_prediction = models.IntegerField()
    land_prediction = models.IntegerField()
    buildings_prediction = models.IntegerField()
    objects = models.Manager()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)


class AI_Objects(models.Model):
    """Objects Table for AI tiled"""

    class Meta:
        """Meta AI objects"""
        app_label = 'core'

    id = models.AutoField(primary_key=True)
    tiles_id = models.ForeignKey(AI_Tiles, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    prediction = models.IntegerField()
    objects = models.Manager()


# Other tables ######################################################

class UsableTiles(models.Model):
    """Tiles that can be used because they are not black"""
    id = models.AutoField(primary_key=True)

    x_coord = models.IntegerField(blank=False)
    y_coord = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
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
