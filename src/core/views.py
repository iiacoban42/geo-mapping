"""Views module"""
# pylint: disable=[unused-argument, fixme, relative-beyond-top-level]

import random

from django.shortcuts import render
from django.http import JsonResponse

from .models import Tiles

# Create your views here.
def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')

def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')

def get_tile(request):
    """Return two object containing: year, x, y"""


    #Pick an unknown tile
    year_new = 2010 # TODO: Support other years
    x_new = -1
    y_new = -1

    while True:
        if year_new == 2010:
            x_new = random.choice(range(75079, 75804))
            y_new = random.choice(range(74990, 76586))

        tile = Tiles.objects.filter(x_coord=x_new, y_coord=y_new)
        if len(tile) == 0:
            break

    #Pick a known tile
    tile = random.choice(Tiles.objects.all())

    year_known = tile.year
    x_known = tile.x_coord
    y_known = tile.y_coord

    response = [{'year': year_new, 'x': x_new, 'y': y_new},
                {'year': year_known, 'x': x_known, 'y': y_known}]
    random.shuffle(response)

    return JsonResponse(response, safe=False)
