from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from . import models
import json


def register_equipment(request):
    if request.method == 'POST':
        models.Equipment(
            serial_number=request.POST.get('serial_number'),
            uid=request.POST.get('uid'),
            type=request.POST.get('type'),
            type_id=request.POST.get('type_id'),
        ).save()

        return render(request, 'equipment/register-equipment.html', {'message': 'Equipamento cadastrado com sucesso'})
    else:
        return render(request, 'equipment/register-equipment.html')

# Retorna o UID mais recente em formato JSON


def get_equipment(request):
    if settings.AUX['UID'] != '':
        equipment = models.Equipment.objects.filter(
            uid=settings.AUX['UID']).first()
        armament = models.Armament.objects.all()
        wearable = models.Wearable.objects.all()

        data = {
            'uid': settings.AUX['UID'],
            'registred': False,
            'Armament': '',
            'Wearable': '',
        }

        if equipment is None:
            data['Armament'] = serializers.serialize('python', armament)
            data['Wearable'] = serializers.serialize('python', wearable)
        elif equipment.type == 'Armament':
            armament = models.Armament.objects.filter(pk=equipment.type_id)
            data['registred'] = equipment.type
            data['equipment'] = equipment
            data['Armament'] = serializers.serialize('python', armament)
        elif equipment.type == 'Wearable':
            wearable = models.Wearable.objects.filter(pk=equipment.type_id)
            data['registred'] = equipment.type
            data['equipment'] = equipment
            data['Wearable'] = serializers.serialize('python', wearable)

        if settings.AUX['UID'] != '':
            settings.AUX['UID'] = ""
    else:
        data = {
            'uid': settings.AUX['UID'],
            'registred': True,
        }
    return JsonResponse(data)


# Recebe o UID do ESP


def set_uid(request):
    # Armazena o UID recebido numa variável global no arquivo settings
    if request.method == 'POST':
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.POST.get('uid')
    elif request.method == 'GET':
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.GET.get('uid')

    return HttpResponse(f"Sucesso, uid = {settings.AUX['UID']}")
