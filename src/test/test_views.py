"""Test views"""
from django.test import TestCase, Client
from django.urls import reverse
# pylint: disable=all


# Create your tests here.
class TestViews(TestCase):

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
