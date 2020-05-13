"""Core urls module"""
from django.urls import path
from . import views

# pylint: disable=all

urlpatterns = [
    path('captcha/', views.captcha),
    path('get_tile/', views.get_tile),
    path('', views.home)
]
