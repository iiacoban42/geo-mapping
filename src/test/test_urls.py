"""Test urls"""
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from core.views import *


# pylint: disable=all

# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_index(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)

    def test_tiles_overview(self):
        url = reverse('tiles_overview')
        print(resolve(url))
        self.assertEquals(resolve(url).func, tiles_overview)

    def test_get_statistics(self):
        url = reverse('get_statistics')
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_statistics)

    def test_get_tile(self):
        url = reverse('get_tile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_tile)

    def test_get_statistics_year(self):
        url = reverse('get_statistics_year', args=['2010'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_statistics_year)

    def test_captcha(self):
        url = reverse('captcha')
        print(resolve(url))
        self.assertEquals(resolve(url).func, captcha)

