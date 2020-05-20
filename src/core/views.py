"""Views module"""
# pylint: disable=[unused-argument, fixme, relative-beyond-top-level, line-too-long]

import random
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from .models import Tiles, Characteristics, Objects, CaptchaSubmissions

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
        if not tile.exists():
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

def submit_captcha(request):
    """Verify captcha challenge"""
    submission = json.loads(request.body)
    print(submission[0])

    #Find which tile is the control
    tile1_query = Tiles.objects.filter(x_coord=submission[0]['x'], y_coord=submission[0]['y'],
                                       year=submission[0]['year'])
    tile2_query = Tiles.objects.filter(x_coord=submission[1]['x'], y_coord=submission[1]['y'],
                                       year=submission[1]['year'])

    if len(tile1_query) > 0:
        #Tile #1 is control, verify it's data
        control_tile = tile1_query[0]
        control_sub = submission[0]
        unid_sub = submission[1]
    elif len(tile2_query) > 0:
        #Tile #2 is control, verify it's data
        control_tile = tile2_query[0]
        control_sub = submission[1]
        unid_sub = submission[0]
    else:
        return HttpResponseBadRequest("No tile")

    char_query = Characteristics.objects.filter(tiles_id=control_tile.id)
    if len(char_query) == 0:
        return HttpResponseBadRequest("No characteristics")

    control_char = char_query[0]
    # Check the characteristics
    if (((control_char.water_prediction >= 50) == control_sub['water']) and
            ((control_char.buildings_prediction >= 50) == control_sub['building']) and
            ((control_char.land_prediction >= 50) == control_sub['land'])):
        obj_query = Objects.objects.filter(tiles_id=control_tile.id)
        if len(obj_query) == 0:
            if not control_sub['church'] and not control_sub['oiltank']: # In case there are no objects
                correct_captcha(unid_sub)
                return HttpResponse()
            else:
                return HttpResponseBadRequest("Wrong answer")

        for obj in obj_query.all():
            if ((obj.type == "church" and not control_sub['church']) or
                    (obj.type == "oiltank" and not control_sub['oiltank'])):
                    return HttpResponseBadRequest("Wrong answer")

        correct_captcha(unid_sub)
        return HttpResponse()
    else:
        return HttpResponseBadRequest("Wrong answer")

def correct_captcha(sub):
    submission = CaptchaSubmissions()
    submission.year = sub['year']
    submission.x_coord = sub['x']
    submission.y_coord = sub['y']
    submission.water = sub['water']
    submission.land = sub['land']
    submission.building = sub['building']
    submission.church = sub['church']
    submission.oiltank = sub['oiltank']
    submission.save()
