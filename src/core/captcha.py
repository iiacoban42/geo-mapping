"""Captcha module"""
# pylint: disable=[unused-argument, fixme, relative-beyond-top-level, line-too-long, too-many-branches, too-many-return-statements]

from django.db.models import Avg, Count, FloatField
from django.db.models.functions import Cast

from core.models import CaptchaSubmissions as CaptchaTable
from core.models import ConfirmedCaptchas as ConfirmedCaptchasTable


def check_characteristics(sub, db_tile):
    """Check if characteristics match"""

    if (((db_tile.water_prediction >= 50) == sub['water']) and
            ((db_tile.buildings_prediction >= 50) == sub['building']) and
            ((db_tile.land_prediction >= 50) == sub['land'])):

        return True

    return False


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
