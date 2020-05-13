"""Serializers module"""
# translates objects from the database in json objects
# fields specify json fields that are returned as a response to an HTTP request
# pylint: disable=all

from rest_framework import serializers
from .models import Tiles, Objects, Characteristics


class TileSerializer(serializers.ModelSerializer):
    """Tile serializer"""

    class Meta:
        """Tile meta"""
        model = Tiles
        fields = ('year', 'x_coord', 'y_coord')


class ObjectSerializer(serializers.ModelSerializer):
    """Tile object serializer"""

    class Meta:
        """Object meta"""
        model = Objects
        fields = ('type', 'x_coord', 'y_coord', 'prediction')


class CharacteristicsSerializer(serializers.ModelSerializer):
    """Tile characteristics serializer"""

    class Meta:
        """Characteristics meta"""
        model = Characteristics
        fields = ('water_prediction', 'land_prediction', 'buildings_prediction')
