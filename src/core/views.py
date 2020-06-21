"""Views module"""
# pylint: disable=[line-too-long,import-error, unused-argument, no-name-in-module,wildcard-import, fixme]

import json
import random
from datetime import datetime, timedelta

import pytz
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from pyproj import Transformer

from core.captcha import pick_unsolved_captcha, pick_random_captcha, find_tiles, check_characteristics, \
    check_objects
#from core.detection import detect
from core.models import AI_Tiles as AITilesTable, AI_Characteristics, AI_Objects
from core.models import Captcha_Tiles as CaptchaTable
from core.models import Confirmed_Captcha_Characteristics as ConfirmedCaptchaChars
from core.models import Confirmed_Captcha_Tiles as ConfirmedCaptchaTiles
from core.models import Dataset as DatasetTable

X_WIDTH = 406.29705
X_OFFSET = -30507572.70109
Y_HEIGHT = -406.89159
Y_OFFSET = 31149422.11094

def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')


def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')


def tiles_overview(request):
    """render tiles_overview.html page"""

    return render(request, 'tiles-overview/tiles_overview.html')


@xframe_options_exempt
def captcha_embed(request):
    """render captcha_embed.html page"""

    return render(request, 'captcha/captcha_embed.html')


@xframe_options_exempt
def embed_example(request):
    """render embed_example.html page"""

    return render(request, 'captcha/embed_example.html')


def get_statistics(request):
    """send statistics json"""
    ai_tiles = AITilesTable.objects.all().count()
    cap = CaptchaTable.objects.all().count()
    dataset = DatasetTable.objects.all().count()
    response = {'ai': ai_tiles, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_statistics_year(request, requested_year):
    """send statistics json by year"""
    ai_tiles = AITilesTable.objects.filter(year=requested_year).count()
    cap = CaptchaTable.objects.filter(year=requested_year).count()
    dataset = DatasetTable.objects.filter(year=requested_year).count()
    response = {'ai': ai_tiles, 'cap': cap, 'dataset': dataset}
    return JsonResponse(response, safe=False)


def get_markers(request):
    """Return json array of markers"""

    data = {}
    data['labels'] = []
    data['points'] = []
    for obj in AI_Objects.objects.all():
        data['labels'].append({"Label": "Label", "Name": obj.type, "Other": "-"})

        # Linear regression magic (can be a few meters off, might improve with more data later)
        x_28992 = obj.x_coord * X_WIDTH + X_OFFSET
        y_28992 = obj.y_coord * Y_HEIGHT + Y_OFFSET

        # Center
        x_28992 += X_WIDTH / 2
        y_28992 -= Y_HEIGHT / 2

        # Transform to 'world' coordinates
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        espg_4326 = transformer.transform(x_28992, y_28992)

        data['points'].append({'type': "point", 'longitude': str(espg_4326[1]), 'latitude': str(espg_4326[0])})
    return JsonResponse(data, safe=False)


def get_labels(request, tile):
    """Return the labels of a tile stored in DatasetTable"""
    query = json.loads(tile)
    tile = DatasetTable.objects.filter(year=query.get("year"), x_coord=query.get("x_coord"),
                                       y_coord=query.get("y_coord")).all()
    if len(tile) == 0:
        res = {'land': 0, 'water': 0, 'building': 0}
        return JsonResponse(res, safe=False)
    response = {'land': tile[0].land, 'water': tile[0].water, 'building': tile[0].building}
    return JsonResponse(response, safe=False)


def get_all_labels(request, requested_map):
    """Return json array of tiles with a specific label"""
    transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
    query = json.loads(requested_map)
    tiles = AITilesTable.objects.filter(year=query.get("year"))
    if len(tiles) == 0:
        return HttpResponseBadRequest("No tiles")
    result = []
    label = str(query.get("label"))
    if label not in ("building", "water", "land", "church"):
        return HttpResponseBadRequest("Wrong Label")

    if label not in ["church"]:
        if label == "building":
            label += "s"
        label += "_prediction"
        kwargs = {label: 1}
        ids = AI_Characteristics.objects.filter(pk__in=tiles.all().values_list('id', flat=True), **kwargs)
        if len(ids) == 0:
            return HttpResponseBadRequest("No tiles")
        for tile in tiles.filter(pk__in=ids.all()):
            # Linear regression magic (can be a few meters off, might improve with more data later)
            x_28992 = tile.x_coord * X_WIDTH + X_OFFSET
            y_28992 = tile.y_coord * Y_HEIGHT + Y_OFFSET

            # Center
            x_28992 += X_WIDTH / 2
            y_28992 -= Y_HEIGHT / 2

            espg_4326 = transformer.transform(x_28992, y_28992)
            result.append({"x_coord": espg_4326[1], "y_coord": espg_4326[0]})
    else:
        ids = AI_Objects.objects.filter(tiles_id__in=tiles.all().values_list('id', flat=True))
        if len(ids) == 0:
            return HttpResponseBadRequest("No tiles")
        for tile in tiles.filter(pk__in=ids.values_list('tiles_id', flat=True)):
            # Linear regression magic (can be a few meters off, might improve with more data later)
            x_28992 = tile.x_coord * X_WIDTH + X_OFFSET
            y_28992 = tile.y_coord * Y_HEIGHT + Y_OFFSET

            # Center
            x_28992 += X_WIDTH / 2
            y_28992 -= Y_HEIGHT / 2
            espg_4326 = transformer.transform(x_28992, y_28992)
            result.append({"x_coord": espg_4326[1], "y_coord": espg_4326[0]})

    return JsonResponse(result, safe=False)


def get_tile(request):
    """Return two object containing: year, x, y"""

    (year_new, x_new, y_new) = pick_unsolved_captcha()

    if year_new == -1:  # If all current captchas are solved, pick a random new challenge
        print("Out of challenges. Picking random unsolved from usable")
        (year_new, x_new, y_new) = pick_random_captcha()

    if year_new == -1:  # If there are no usable tiles, return empty
        return HttpResponse()

    # Pick a known tile
    tile = random.choice(ConfirmedCaptchaTiles.objects.all())

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

    # Find which tile is the control
    control = find_tiles(submission)
    if control == 0:
        return HttpResponseBadRequest("No tile")

    control_tile = control[0]
    control_sub = control[1]
    unid_sub = control[2]

    char_query = ConfirmedCaptchaChars.objects.filter(tiles_id=control_tile.id)
    if len(char_query) == 0:
        return HttpResponseBadRequest("No characteristics")
    control_char = char_query[0]

    # Check the characteristics
    if check_characteristics(control_sub, control_char):
        result = check_objects(control_sub, unid_sub, control_tile)
        if result is not None:
            return HttpResponse(result)
    return HttpResponseBadRequest("Wrong answer")


def get_accuracy(request):
    """Get last accuracy of CNN"""
    with open('static/history.txt') as file:
        read_data = {'accuracy': file.read()[1:-1]}
        print(read_data)
        file.close()
        return JsonResponse(read_data, safe=False)


def train(request):
    """Return timestamp of the most recently classified tile"""
    latest_forecast = AI_Characteristics.objects.latest('timestamp')

    timestamp = "{t.year}/{t.month:02d}/{t.day:02d} - {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(
        t=latest_forecast.timestamp + timedelta(hours=2))
    print(datetime.now(tz=pytz.utc))
    return render(
        request,
        'train/train.html',
        {'accuracy': None,
         'update_time': timestamp})


def machine_learning(request):
    """Train CNN and update timestamp"""

    # !!!!!!! LEFT MINUTES TO TEST
    a_week_ago = datetime.now(tz=pytz.utc) - timedelta(minutes=0)
    # UNCOMMENT TO BE ABLE TO RUN THE ML BY PRESSING THE BUTTON (AT /train) ONCE EVERY 7 DAYS
    # a_week_ago = datetime.now(tz=pytz.utc) - timedelta(days=7)
    latest_forecast = AI_Characteristics.objects.latest('timestamp')
    if latest_forecast is None or (latest_forecast.timestamp < a_week_ago):
        detect.run()
        latest_forecast = AI_Characteristics.objects.latest('timestamp')
        timestamp = "{t.year}/{t.month:02d}/{t.day:02d} - {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(
            t=latest_forecast.timestamp + timedelta(hours=2))
        print('FORECAST UPDATED', timestamp)
        return JsonResponse(timestamp, safe=False)
    return HttpResponseBadRequest("Too little time passed")
