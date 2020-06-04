"""Views module"""
# pylint: disable=[unused-argument, fixme, relative-beyond-top-level, line-too-long, too-many-branches, too-many-return-statements]

import random
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.db.models import Avg, Count, FloatField
from django.db.models.functions import Cast

from pyproj import Transformer

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import Dataset as DatasetTable
from core.models import Tiles as TileTable
from core.models import Characteristics as CharacteristicsTable
from core.models import Objects as ObjectsTable
from core.models import ConfirmedCaptchas as ConfirmedCaptchasTable


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

    data = {}
    data['labels'] = []
    data['points'] = []
    for obj in ObjectsTable.objects.all():
        data['labels'].append({"Label": "Label", "Name": obj.type, "Other": "-"})

        # Linear regression magic (can be a few meters off, might improve with more data later)
        x_28992 = obj.tiles_id.x_coord * 406.55828 - 30527385.66843
        y_28992 = obj.tiles_id.y_coord * -406.41038 + 31113121.21698

        #Center
        x_28992 += 203
        y_28992 -= 203

        # Transorm to 'world' coordinates
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        espg_4326 = transformer.transform(x_28992, y_28992)

        print(x_28992, y_28992)
        data['points'].append({'type': "point",'longitude': str(espg_4326[1]), 'latitude': str(espg_4326[0])})
    print(data)
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
    print(submission[0])

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
    if (((control_char.water_prediction >= 50) == control_sub['water']) and
            ((control_char.buildings_prediction >= 50) == control_sub['building']) and
            ((control_char.land_prediction >= 50) == control_sub['land'])):
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


def correct_captcha(sub):
    """When a correct control challenge is submitted, the unknown map tile result is recorded"""
    submission = CaptchaTable()
    submission.year = sub['year']
    submission.x_coord = sub['x']
    submission.y_coord = sub['y']
    submission.water = sub['water']
    submission.land = sub['land']
    submission.building = sub['building']
    submission.church = sub['church']
    submission.oiltank = sub['oiltank']
    submission.save()

    check_submission(submission.year, submission.x_coord, submission.y_coord)


def check_submission(year, x_coord, y_coord):
    """"When multiple people have answered a CAPTCHA in a similar matter, that answer is recorded"""
    submissions_query = CaptchaTable.objects.filter(x_coord=x_coord, y_coord=y_coord, year=year) \
        .aggregate(cnt=Count('*'), avg_water=Avg(Cast('water', FloatField())), avg_land=Avg(Cast('land', FloatField())), \
                   avg_building=Avg(Cast('building', FloatField())), avg_church=Avg(Cast('church', FloatField())), \
                   avg_oiltank=Avg(Cast('oiltank', FloatField())))

    if len(submissions_query) == 0:
        return

    print(submissions_query)
    submissions = submissions_query
    low_bound = 0.2
    high_bound = 0.8

    if submissions['cnt'] < 5:
        print("Not enough votes to classify tile")
        return

    if ((not (submissions['avg_water'] <= low_bound or submissions['avg_water'] >= high_bound)) or \
            (not (submissions['avg_land'] <= low_bound or submissions['avg_land'] >= high_bound)) or \
            (not (submissions['avg_building'] <= low_bound or submissions['avg_building'] >= high_bound)) or \
            (not (submissions['avg_church'] <= low_bound or submissions['avg_church'] >= high_bound)) or \
            (not (submissions['avg_oiltank'] <= low_bound or submissions['avg_oiltank'] >= high_bound))):
        print("Votes are too different to classify tile")
        return

    confirmed = ConfirmedCaptchasTable()
    confirmed.x_coord = x_coord
    confirmed.y_coord = y_coord
    confirmed.year = year

    confirmed.water_prediction = (submissions['avg_water']) * 100
    confirmed.land_prediction = (submissions['avg_land']) * 100
    confirmed.buildings_prediction = (submissions['avg_building']) * 100
    confirmed.church_prediction = (submissions['avg_church']) * 100
    confirmed.oiltank_prediction = (submissions['avg_oiltank']) * 100

    confirmed.save()
