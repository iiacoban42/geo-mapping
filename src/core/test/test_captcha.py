"""Integration tests between database and server (captcha)"""
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


class TestCaptcha(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        tile = TileTable()
        tile.x_coord = 0
        tile.y_coord = 0
        tile.year = 2010
        tile.save()

        chars = CharacteristicsTable()
        chars.tiles_id = tile
        chars.water_prediction = 100
        chars.land_prediction = 0
        chars.buildings_prediction = 0
        chars.save()

        tile2 = TileTable()
        tile2.x_coord = 2
        tile2.y_coord = 2
        tile2.year = 2014
        tile2.save()

        obj = ObjectsTable()
        obj.tiles_id = tile2
        obj.x_coord = 0
        obj.y_coord = 0
        obj.prediction = 100
        obj.type = 'oiltank'
        obj.save()
        ConfirmedCaptchasTable()
        CaptchaTable()

    def test_get_tile(self):
        # Create an instance of a GET request.
        request = self.factory.get('get_tile')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_tile(request)
        self.assertEqual(response.status_code, 200)

    def test_valid_captcha(self):
        submission = '[{"year":2010, "x":0, "y":0, "building":false, "water":true, "land":false, "church":false, "oiltank":false},' \
                     ' {"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 200)

    def test_valid_captcha_reverse_order(self):
        submission = '[{"year":2010, "x":1, "y":1, "building":true, "water":false,"land":true, "church":false, "oiltank":false}, ' \
                     '{"year":2010, "x":0, "y":0, "building":false, "water":true, "land":false, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_captcha(self):
        submission = '[{"year":2010, "x":0, "y":0, "building":true, "water":true, "land":false, "church":false, "oiltank":false},' \
                     ' {"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_check_captcha(self):
        submission = '[{"year":2014, "x":0, "y":0, "building":true, "water":true, "land":false, "church":false, "oiltank":false},' \
                     ' {"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_captcha_no_chars(self):
        submission = '[{"year":2014, "x":2, "y":2, "building":true, "water":true, "land":false, "church":false, "oiltank":false}, ' \
                     '{"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 400)

    def test_valid_captcha_objects(self):
        stored_tile2 = TileTable.objects.filter(x_coord=2, y_coord=2,
                                                year=2014)
        chars = CharacteristicsTable()
        chars.tiles_id = stored_tile2[0]
        chars.water_prediction = 100
        chars.land_prediction = 0
        chars.buildings_prediction = 0
        chars.save()

        submission = '[{"year":2014, "x":2, "y":2, "building":false, "water":true, "land":false, "church":false, "oiltank":true}, ' \
                     '{"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_captcha_objects(self):
        stored_tile2 = TileTable.objects.filter(x_coord=2, y_coord=2,
                                                year=2014)
        chars = CharacteristicsTable()
        chars.tiles_id = stored_tile2[0]
        chars.water_prediction = 100
        chars.land_prediction = 0
        chars.buildings_prediction = 0
        chars.save()

        submission = '[{"year":2014, "x":2, "y":2, "building":false, "water":true, "land":false, "church":false, "oiltank":false}, ' \
                     '{"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_captcha_objects2(self):
        submission = '[{"year":2010, "x":0, "y":0, "building":false, "water":true, "land":false, "church":true, "oiltank":true}, ' \
                     '{"year":2010, "x":1, "y":1, "building":true, "water":false, "land":true, "church":false, "oiltank":false}]'

        sub = json.loads(submission)
        # Create an instance of a POST request.
        request = self.factory.post(path='submit_captcha', data=sub, content_type='application/json')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = submit_captcha(request)
        self.assertEqual(response.status_code, 400)
