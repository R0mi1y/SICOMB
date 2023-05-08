from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from . import models
from django.forms.models import model_to_dict
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
        try:
            equipment = models.Equipment.objects.get(
                uid=settings.AUX['UID'])
        except models.Equipment.DoesNotExist:
            equipment = None

        armament = models.Armament.objects.all()
        wearable = models.Wearable.objects.all()

        set_armament = {}
        set_wearable = {}

        cont = 0
        for i in armament:
            set_armament['armamento ' + str(i.pk)] = model_to_dict(i)
            cont = + 1
        cont = 0
        for i in wearable:
            set_wearable['vestivel ' + str(i.pk)] = model_to_dict(i)
            cont = + 1

        data = {
            'uid': settings.AUX['UID'],
            'registred': False,
            'Armament': '',
            'Wearable': '',
        }

        if equipment is None:
            data['Armament'] = set_armament
            data['Wearable'] = set_wearable

            print(str(data) + " Equipamento não cadastrado")
        elif equipment.type == 'Armament':
            armament = models.Armament.objects.get(pk=equipment.type_id)
            data['registred'] = equipment.type
            data['equipment'] = model_to_dict(equipment)
            data['Armament'] = model_to_dict(armament)

            print("Equipamento é um armamento")
        elif equipment.type == 'Wearable':
            wearable = models.Wearable.objects.get(pk=equipment.type_id)
            data['registred'] = equipment.type
            data['equipment'] = model_to_dict(equipment)
            data['Wearable'] = model_to_dict(wearable)

            print("Equipamento é um vestível")

        if settings.AUX['UID'] != '':
            settings.AUX['UID'] = ""
    else:
        data = {
            'uid': settings.AUX['UID'],
            'registred': True,
        }

        print("uid não inserido")
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
