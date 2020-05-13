"""Views module"""
from django.shortcuts import render
from django.http import JsonResponse
import random

# Create your views here.

def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')

def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')

def get_tile(request):
    """Return object containing: year, x, y"""
    year = 2010 # TODO: Support other years
    x = -1
    y = -1

    if year == 2010:
        x = random.choice(range(75079,75804))
        y = random.choice(range(74990,76586))

    return JsonResponse({'year': year, 'x': x, 'y': y})
