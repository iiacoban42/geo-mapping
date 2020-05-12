"""Views module"""
from django.shortcuts import render


# Create your views here.

def home(request):
    """render index.html page"""
    return render(request, 'maps/main.html')

def captcha(request):
    """render captcha.html page"""
    return render(request, 'captcha/captcha.html')
