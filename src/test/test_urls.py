"""Test urls"""
from django.test import TestCase
from django.urls import resolve, reverse
from core.views import home, captcha
# pylint: disable=all

# Create your tests here.
class TestUrls(TestCase):
    def test_index(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)

    def test_captcha(self):
        url = reverse('captcha')
        print(resolve(url))
        self.assertEquals(resolve(url).func, captcha)
