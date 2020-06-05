"""Views module"""
# pylint: disable=[unused-argument, fixme, relative-beyond-top-level, line-too-long, too-many-branches, too-many-return-statements]

import random
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import Dataset as DatasetTable
from core.models import Tiles as TileTable
from core.models import Characteristics as CharacteristicsTable
from core.models import Objects as ObjectsTable
from core.models import ConfirmedCaptchas as ConfirmedCaptchasTable
from core.captcha import *


# Create your views here.


def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')


def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')


def tiles_overview(request):
    """render tiles_overview.html page"""

    return render(request, 'tiles-overview/tiles_overview.html')


def get_statistics(request):
    """send statistics json"""
    # TODO: statistics for ai
    cap = CaptchaTable.objects.all().count()
    dataset = DatasetTable.objects.all().count()
    response = {'ai': 0, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_statistics_year(request, requested_year):
    """send statistics json by year"""
    # TODO: statistics for ai
    cap = CaptchaTable.objects.filter(year=requested_year).count()
    dataset = DatasetTable.objects.filter(year=requested_year).count()
    response = {'ai': 0, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_markers(request):
    """Return json array of markers"""
    with open("core/json/points.json", 'r') as markers:
        data = markers.read()
    return JsonResponse(data, safe=False)


def get_tile(request):
    """Return two object containing: year, x, y"""

    # Pick an unknown tile
    year_new = 2010  # TODO: Support other years
    x_new = -1
    y_new = -1

    while True:
        if year_new == 2010:
            x_new = random.choice(range(75079, 75804))
            y_new = random.choice(range(74990, 76586))

        tile = TileTable.objects.filter(x_coord=x_new, y_coord=y_new)
        if len(tile) > 0:
            continue

        tile_confirmed = ConfirmedCaptchasTable.objects.filter(x_coord=x_new, y_coord=y_new, year=year_new)

        if len(tile_confirmed) > 0:
            continue

        break

    # Pick a known tile
    tile = random.choice(TileTable.objects.all())

    year_known = tile.year
    x_known = tile.x_coord
    y_known = tile.y_coord

    response = [{'year': year_new, 'x': x_new, 'y': y_new},
                {'year': year_known, 'x': x_known, 'y': y_known}]
    random.shuffle(response)

    return JsonResponse(response, safe=False)


def submit_captcha(request):
    """Verify captcha challenge"""
    # NOTE: Terrible code ahead. I'll try to make it prettier later on. -Georgi
    submission = json.loads(request.body)
    print(submission)

    # Find which tile is the control
    tile1_query = TileTable.objects.filter(x_coord=submission[0]['x'], y_coord=submission[0]['y'],
                                           year=submission[0]['year'])
    tile2_query = TileTable.objects.filter(x_coord=submission[1]['x'], y_coord=submission[1]['y'],
                                           year=submission[1]['year'])
    if len(tile1_query) > 0:
        # Tile #1 is control, verify it's data
        control_tile = tile1_query[0]
        control_sub = submission[0]
        unid_sub = submission[1]
    elif len(tile2_query) > 0:
        # Tile #2 is control, verify it's data
        control_tile = tile2_query[0]
        control_sub = submission[1]
        unid_sub = submission[0]
    else:
        return HttpResponseBadRequest("No tile")

    char_query = CharacteristicsTable.objects.filter(tiles_id=control_tile.id)
    if len(char_query) == 0:
        return HttpResponseBadRequest("No characteristics")
    control_char = char_query[0]

    # Check the characteristics
    if check_characteristics(control_sub, control_char):
        obj_query = ObjectsTable.objects.filter(tiles_id=control_tile.id)
        if len(obj_query) == 0:
            if not control_sub['church'] and not control_sub['oiltank']:  # In case there are no objects
                correct_captcha(unid_sub)
                return HttpResponse()
            return HttpResponseBadRequest("Wrong answer")

        for obj in obj_query.all():
            if ((obj.type == "church" and not control_sub['church']) or
                    (obj.type == "oiltank" and not control_sub['oiltank'])):
                return HttpResponseBadRequest("Wrong answer")

        correct_captcha(unid_sub)
        return HttpResponse()
    return HttpResponseBadRequest("Wrong answer")
