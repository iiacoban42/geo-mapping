"""Test requests from views"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import Tiles as TileTable
from core.models import Characteristics as CharacteristicsTable
from core.models import Objects as ObjectsTable
from core.models import ConfirmedCaptchas as ConfirmedCaptchasTable

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all


# Create your tests here.
from src.core.views import *


class TestRequests(TestCase):
    submission = "[{'year': 2010, 'x': 75296, 'y': 75488, 'building': True, 'water': True, 'land': False, 'church': False, 'oiltank': True}, {'year': 2010, 'x': 75578, 'y': 75422, 'building': True, 'water': False, 'land': True, 'church': False, 'oiltank': False}]"

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        tile = TileTable()
        tile.x_coord = 75296
        tile.y_coord = 75488
        tile.year = 2010
        tile.save()

        stored_tile = TileTable.objects.filter(x_coord=75296, y_coord=75488,
                                               year=2010)

        chars = CharacteristicsTable()
        chars.tiles_id = stored_tile[0]
        chars.water_prediction = 100
        chars.land_prediction = 0
        chars.buildings_prediction = 100
        chars.save()

        obj = ObjectsTable()
        obj.tiles_id = stored_tile[0]
        obj.x_coord = 0
        obj.y_coord = 0
        obj.prediction = 100
        obj.type = 'oiltank'
        obj.save()
        ConfirmedCaptchasTable()
        CaptchaTable()

    def test_get_statistics(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_statistics_year')

        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = get_statistics(request)
        self.assertEqual(response.status_code, 200)

    def test_get_statistics_year(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_statistics_year')

        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = get_statistics_year(request, requested_year=2010)
        self.assertEqual(response.status_code, 200)

    def test_get_tile(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_tile')

        # an AnonymousUser instance.
        request.user = AnonymousUser()

        response = get_tile(request)
        self.assertEqual(response.status_code, 200)

    # def test_submit_captcha(self):
    #     submission = '[{"year": "2010", "x": "75296", "y": "75488", "building": "True", "water": "True", "land": "False", "church": "False", "oiltank": "True"}, {"year": "2010", "x": "75578", "y": "75422", "building": "True", "water": "False", "land": "True", "church": "False", "oiltank": "False"}]'
    #
    #     sub = json.loads(submission)
    #     # Create an instance of a POST request.
    #     request = self.factory.post(path='submit_captcha', data=sub, format='json')
    #
    #     # an AnonymousUser instance.
    #     request.user = AnonymousUser()
    #
    #     response = submit_captcha(request)
    #     self.assertEqual(response.status_code, 200)
