"""Captcha module"""
# pylint: disable=[line-too-long, import-error, no-name-in-module]
import random
from django.db.models import Avg, Count, FloatField
from django.db.models.functions import Cast

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import Tiles as TileTable
from core.models import ConfirmedCaptchas as ConfirmedCaptchasTable
from core.models import Objects as ObjectsTable


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
            correct_captcha(unid_sub)
            return True
        return False

    for obj in obj_query.all():
        if ((obj.type == "church" and not control_sub['church']) or
                (obj.type == "oiltank" and not control_sub['oiltank'])):
            return False

    correct_captcha(unid_sub)
    return True


def correct_captcha(sub):
    """When a correct control challenge is submitted, the unknown map tile result is recorded"""
    print("correct captcha")
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


def pick_unsolved_captcha():
    """Pick a captcha challenge that has been submitted at least once before,
       but not enough to be confirmed"""

    year_new = -1
    x_new = -1
    y_new = -1

    for challenge in CaptchaTable.objects.order_by('?'):
        tile_confirmed = ConfirmedCaptchasTable.objects.filter(x_coord=challenge.x_coord, y_coord=challenge.y_coord,
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
    year_new = 2010
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

    return (year_new, x_new, y_new)
