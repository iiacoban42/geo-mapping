"""Views module"""
import random

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')

def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')

# pylint: disable=[unused-argument, fixme]
def get_tile(request):
    """Return object containing: year, x, y"""
    year = 2010 # TODO: Support other years
    x_coord = -1
    y_coord = -1

    if year == 2010:
        x_coord = random.choice(range(75079, 75804))
        y_coord = random.choice(range(74990, 76586))

    return JsonResponse({'year': year, 'x': x_coord, 'y': y_coord})
