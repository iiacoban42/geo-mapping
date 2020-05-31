"""Test requests from views"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
import sys
import os

sys.path.append(os.path.join(os.path.dirname("src"), '..'))
# pylint: disable=all


# Create your tests here.
from src.core.views import *


class TestRequests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

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
