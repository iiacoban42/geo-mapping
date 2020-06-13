"""Integration tests between database and server"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

from core.models import Tiles as TileTable
from core.models import Objects as ObjectsTable
from core.models import Dataset as DatasetTable
from core.models import AI_Tiles as AITilesTable
from core.models import AI_Characteristics as AICharsTable

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all


# Create your tests here.
from src.core.views import *


class TestRequests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        tile_ai = AITilesTable()
        tile_ai.x_coord = 2
        tile_ai.y_coord = 2
        tile_ai.year = 2010
        tile_ai.save()

        tile_chars = AICharsTable()
        tile_chars.tiles_id = tile_ai
        tile_chars.land_prediction = 1
        tile_chars.water_prediction = 0
        tile_chars.buildings_prediction = 0
        tile_chars.save()

        tile_ai2 = AITilesTable()
        tile_ai2.x_coord = 1
        tile_ai2.y_coord = 1
        tile_ai2.year = 2011
        tile_ai2.save()

        tile_chars2 = AICharsTable()
        tile_chars2.tiles_id = tile_ai2
        tile_chars2.land_prediction = 0
        tile_chars2.water_prediction = 1
        tile_chars2.buildings_prediction = 1
        tile_chars2.save()

    def test_ai_tiles_land(self):
        submission = '{"year": 2010, "label": "land"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 200)

    def test_ai_tiles_no_tile_water(self):
        submission = '{"year": 2010, "label": "water"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 400)

    def test_ai_tiles_water(self):
        submission = '{"year": 2011, "label": "water"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 200)

    def test_ai_tiles_no_tile_land(self):
        submission = '{"year": 2011, "label": "land"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 400)

    def test_ai_tiles_no_tile_building(self):
        submission = '{"year": 2010, "label": "building"}'

        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 400)

    def test_ai_tiles_building(self):
        submission = '{"year": 2011, "label": "building"}'

        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 200)

    def test_ai_tiles_no_tile_from_label(self):
        submission = '{"year": 2020, "label": "water"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 400)

    def test_ai_tiles_wrong_label(self):
        submission = '{"year": 2010, "label": "church"}'

        sub = json.loads(submission)
        # Create an instance of a GET request.
        request = self.factory.get('get_all_labels')

        # an AnonymousUser instance.
        request.user = AnonymousUser()
        response = get_all_labels(request, submission)
        self.assertEqual(response.status_code, 400)
