"""Smoke test"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

from core.models import Tiles as TileTable
from core.models import Characteristics as CharacteristicsTable

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all


# Create your tests here.
from src.core.views import *


class TestSmoke(TestCase):
    """Test basic functionality with a smoke test"""

    def setUp(self):
        self.factory = RequestFactory()
        tile = TileTable()
        tile.x_coord = 0
        tile.y_coord = 0
        tile.year = 2010
        tile.save()

        stored_tile = TileTable.objects.filter(x_coord=0, y_coord=0,
                                               year=2010)

        chars = CharacteristicsTable()
        chars.tiles_id = stored_tile[0]
        chars.water_prediction = 100
        chars.land_prediction = 0
        chars.buildings_prediction = 0
        chars.save()

    def test_smoke(self):
        # Go to home page
        request = self.factory.get('home')
        request.user = AnonymousUser()
        response = home(request)
        self.assertEqual(response.status_code, 200)

        # Go to tile overview page
        request = self.factory.get('get_statistics')
        response = get_statistics(request)
        self.assertEqual(response.status_code, 200)

        # Go to the CAPTCHA page
        request = self.factory.get('captcha')
        response = captcha(request)
        self.assertEqual(response.status_code, 200)

        # Send a valid CAPTCHA
        submission = '[{"year":2010, "x":0, "y":0, "building":false, "water":true, "land":false, "church":false, "oiltank":false},' \
                     ' {"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 200)
