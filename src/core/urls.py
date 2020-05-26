"""Core urls module"""
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

# pylint: disable=all

urlpatterns = [
    path('captcha/', views.captcha, name='captcha'),
    path('get_tile/', views.get_tile, name='get_tile'),
    path('submit_captcha/', csrf_exempt(views.submit_captcha), name='get_tile'),
    path('tiles_overview/', views.tiles_overview, name='tiles_overview'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    path('', views.home, name='index')
]
