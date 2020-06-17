"""Captcha module"""
# pylint: disable=[line-too-long, import-error, no-name-in-module]
import random
import uuid

from django.db.models import Avg, Count, Q
from django.utils import timezone

from core.models import UsableTiles as UsableTilesTable
from core.models import Tiles as TileTable
from core.models import Objects as ObjectsTable
from core.models import Captcha_Tiles as CaptchaTilesTable
from core.models import Captcha_Characteristics as CaptchaCharsTable
from core.models import Captcha_Objects as CaptchaObjectsTable
from core.models import Confirmed_Captcha_Tiles as ConfirmedCaptchaTiles
from core.models import Confirmed_Captcha_Characteristics as ConfirmedCaptchaChars
from core.models import Confimed_Captcha_Objects as ConfirmedCaptchaObj


def find_tiles(submission):
    """Find which tile is in control"""
    tile1_query = TileTable.objects.filter(x_coord=submission[0]['x'], y_coord=submission[0]['y'],
                                           year=submission[0]['year'])
    tile2_query = TileTable.objects.filter(x_coord=submission[1]['x'], y_coord=submission[1]['y'],
                                           year=submission[1]['year'])
    if len(tile1_query) > 0:
        # Tile #1 is control, verify it's data
        control_tile = tile1_query[0]
        control_sub = submission[0]
        unid_sub = submission[1]
        return [control_tile, control_sub, unid_sub]
    if len(tile2_query) > 0:
        # Tile #2 is control, verify it's data
        control_tile = tile2_query[0]
        control_sub = submission[1]
        unid_sub = submission[0]
        return [control_tile, control_sub, unid_sub]

    return 0


def check_characteristics(sub, db_tile):
    """Check if characteristics match"""

    if (((db_tile.water_prediction >= 50) == sub['water']) and
            ((db_tile.buildings_prediction >= 50) == sub['building']) and
            ((db_tile.land_prediction >= 50) == sub['land'])):
        return True

    return False


def check_objects(control_sub, unid_sub, control_tile):
    """Check if objects match"""
    obj_query = ObjectsTable.objects.filter(tiles_id=control_tile.id)
    if len(obj_query) == 0:
        if not control_sub['church'] and not control_sub['oiltank']:  # In case there are no objects
            return correct_captcha(unid_sub)
        return None

    for obj in obj_query.all():
        if ((obj.type == "church" and not control_sub['church']) or
                (obj.type == "oiltank" and not control_sub['oiltank'])):
            return None

    return correct_captcha(unid_sub)


def correct_captcha(sub):
    """When a correct control challenge is submitted, the unknown map tile result is recorded"""
    print("correct captcha")

    tile = CaptchaTilesTable()
    tile.year = sub['year']
    tile.x_coord = sub['x']
    tile.y_coord = sub['y']
    tile.uuid = uuid.uuid4().hex
    tile.timestamp = timezone.now
    tile.save()

    chars = CaptchaCharsTable()
    chars.tiles_id = tile
    chars.land_prediction = sub['land']
    chars.water_prediction = sub['water']
    chars.buildings_prediction = sub['building']
    chars.save()

    if sub['oiltank']:
        obj = CaptchaObjectsTable()
        obj.tiles_id = tile
        obj.type = 'oiltank'
        obj.prediction = 1
        obj.save()
    if sub['church']:
        obj = CaptchaObjectsTable()
        obj.tiles_id = tile
        obj.type = 'church'
        obj.prediction = 1
        obj.save()

    check_submission(tile.year, tile.x_coord, tile.y_coord)

    return tile.uuid


def check_submission(year, x_coord, y_coord):
    """"When multiple people have answered a CAPTCHA in a similar matter, that answer is recorded"""
    submissions_query = CaptchaTilesTable.objects.filter(x_coord=x_coord, y_coord=y_coord, year=year) \
        .aggregate(cnt=Count('*'), avg_water=Avg('captcha_characteristics__water_prediction'), \
                   avg_land=Avg('captcha_characteristics__land_prediction'), \
                   avg_building=Avg('captcha_characteristics__buildings_prediction'), \
                   cnt_church=Count('captcha_objects__tiles_id', filter=Q(captcha_objects__type="church")), \
                   cnt_oiltank=Count('captcha_objects__tiles_id', filter=Q(captcha_objects__type="oiltank")))

    if len(submissions_query) == 0:
        return

    submissions = submissions_query

    # Calculate average church and oiltank submission
    submissions['avg_church'] = submissions['cnt_church'] / submissions['cnt']
    submissions['avg_oiltank'] = submissions['cnt_oiltank'] / submissions['cnt']


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

    confirmed_tile = ConfirmedCaptchaTiles()
    confirmed_tile.x_coord = x_coord
    confirmed_tile.y_coord = y_coord
    confirmed_tile.year = year
    confirmed_tile.save()

    tile_chars = ConfirmedCaptchaChars()
    tile_chars.tiles_id = confirmed_tile
    tile_chars.water_prediction = (submissions['avg_water']) * 100
    tile_chars.land_prediction = (submissions['avg_land']) * 100
    tile_chars.buildings_prediction = (submissions['avg_building']) * 100
    tile_chars.save()

    if ((submissions['avg_church']) * 100) > 0:
        tile_obj = ConfirmedCaptchaObj()
        tile_obj.tiles_id = confirmed_tile
        tile_obj.type = 'church'
        tile_obj.prediction = (submissions['avg_church']) * 100
        tile_obj.save()

    if ((submissions['avg_oiltank']) * 100) > 0:
        tile_obj = ConfirmedCaptchaObj()
        tile_obj.tiles_id = confirmed_tile
        tile_obj.type = 'oiltank'
        tile_obj.prediction = (submissions['avg_oiltank']) * 100
        tile_obj.save()


def pick_unsolved_captcha():
    """Pick a captcha challenge that has been submitted at least once before,
       but not enough to be confirmed"""

    year_new = -1
    x_new = -1
    y_new = -1

    for challenge in CaptchaTilesTable.objects.order_by('?'):
        tile_confirmed = ConfirmedCaptchaTiles.objects.filter(x_coord=challenge.x_coord, y_coord=challenge.y_coord,
                                                              year=challenge.year)

        if len(tile_confirmed) > 0:
            continue

        year_new = challenge.year
        x_new = challenge.x_coord
        y_new = challenge.y_coord
        break

    return (year_new, x_new, y_new)


def pick_random_captcha():
    """Pick a random captcha challenge that hasn't been submitted (or confirmed) yet"""

    year_new = -1
    x_new = -1
    y_new = -1

    if not UsableTilesTable.objects.all():
        return (year_new, x_new, y_new)

    while True:

        tile = random.choice(UsableTilesTable.objects.all())
        x_new = tile.x_coord
        y_new = tile.y_coord
        year_new = tile.year

        tile_confirmed = ConfirmedCaptchaTiles.objects.filter(x_coord=x_new, y_coord=y_new, year=year_new)

        if len(tile_confirmed) > 0:
            continue

        break

    return (year_new, x_new, y_new)
