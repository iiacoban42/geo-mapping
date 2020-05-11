from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib


def view_index(request):
    index = open('templates/index.html').read()
    return HttpResponse(index)

# def view_index(request):
#     data = {
#         'name': 'john',
#         'message': 'hi'
#     }
#     return JsonResponse(data)
