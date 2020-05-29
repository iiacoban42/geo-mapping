"""Test requests from views"""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from mixer.backend.django import mixer
from src.core.views import *
import pytest

# pylint: disable=all


# Create your tests here.


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def dataset():
    return mixer.blend('core.Dataset')


def test(factory, dataset, db):
    path = reverse('get_statistics_year', args=['2010'])
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_statistics_year(request, requested_year=2010)
    assert response.status_code == 200


def test_stat(factory, dataset, db):
    path = reverse('get_statistics')
    request = factory.get(path)
    request.user = AnonymousUser()

    response = get_statistics(request)
    json = response.json()
    print(json)
    assert json.ai >= 0
    assert json.captcha >= 0
    assert json.dataset >= 0
    assert response.status_code == 200
