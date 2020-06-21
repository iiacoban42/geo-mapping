"""Test views train page"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

from core.models import AI_Tiles as AITilesTable
from core.models import AI_Characteristics as AICharsTable
from core.models import AI_Objects as AIObjTable

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all

from src.core.views import *


# Create your tests here.
class TestViews(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        tile_ai = AITilesTable()
        tile_ai.x_coord = 2
        tile_ai.y_coord = 2
        tile_ai.year = 2010
        tile_ai.save()

        tile_obj = AIObjTable()
        tile_obj.tiles_id = tile_ai
        tile_obj.x_coord = 0
        tile_obj.y_coord = 0
        tile_obj.prediction = 100
        tile_obj.type = 'oiltank'
        tile_obj.save()

        tile_chars = AICharsTable()
        tile_chars.tiles_id = tile_ai
        tile_chars.land_prediction = 1
        tile_chars.water_prediction = 0
        tile_chars.buildings_prediction = 0
        tile_chars.save()

    def test_get_accuracy(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_accuracy')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_accuracy(request)
        self.assertEqual(response.status_code, 200)

    def test_train(self):
        # Create an instance of a GET request.
        request = self.factory.get('train')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = train(request)
        self.assertEqual(response.status_code, 200)
