from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class ViewIndex(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'name': 'john',
            'message': 'hi'
        }
        return Response(data)

# def view_index(request):
#     data = {
#         'name': 'john',
#         'message': 'hi'
#     }
#     return JsonResponse(data)
