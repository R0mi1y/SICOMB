from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from . import models
# Create your views here.

#Método para pegar o policial
def get_policeman(request):
    if settings.DIGITAL_FIGER_POLICEMAN['DIGITAL_FINGER'] != '':
         
        try:
            policeman = models.Police.objects.get(
                digital_finger=settings.DIGITAL_FIGER_POLICEMAN['DIGITAL_FINGER'])
            data = {
                'registred': True,
                'name': policeman.name,
                'patent': policeman.patent,
                'plate': policeman.plate,
                'password': '',
            }
        except models.Police.DoesNotExist:
            policeman = None
            data = {
                'registred': False,
                'name': None,
                'patent': None,
                'plate': None,
                'password': None,
            } 
              
        
    else:
        data = {
        'digital_finger': settings.DIGITAL_FIGER_POLICEMAN['DIGITAL_FINGER'],
        'registred': True,
        }

        print("Digital não inserida")
        
    return JsonResponse(data)