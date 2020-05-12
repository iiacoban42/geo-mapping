"""Core urls module"""
from django.urls import path
from . import views

# pylint: disable=all

urlpatterns = [
    path('', views.home),

]
