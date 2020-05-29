"""Test views html templates"""
from django.test import SimpleTestCase, Client
from django.urls import reverse


# pylint: disable=all


# Create your tests here.
class TestViews(SimpleTestCase):

    def test_index(self):
        self.client = Client()
        self.list_url = reverse('index')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'maps/main.html')

    def test_captcha(self):
        self.client = Client()
        self.list_url = reverse('captcha')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'captcha/captcha.html')

    def test_tiles_overview(self):
        self.client = Client()
        self.list_url = reverse('tiles_overview')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tiles-overview/tiles_overview.html')


