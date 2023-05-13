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

        data = {
            'uid': settings.AUX['UID'],
            'registred': False,
            # 'Armament': '',
            # 'Wearable': '',
        }
        
        types = ["armament", "wearable", "bullet"]

        if equipment is None:
            
            for tipo in types:
                code = (f"{tipo} = models.Model_{tipo}.objects.all() \n" +
                        f"set_{tipo} = " + "{} \n" + 
                        f"for i in {tipo}: \n" + 
                        f"   set_{tipo}['{tipo}' + str(i.pk)] = model_to_dict(i)\n" + 
                        f"data['{tipo.capitalize()}'] = set_{tipo}\n" + 
                        'print(str(data) + " Equipamento não cadastrado")\n')
                print (code)
                exec(code)
        else:
            if equipment.type == 'Armament':
                armament = models.Model_armament.objects.get(pk=equipment.type_id)
                data['registred'] = equipment.type
                data['equipment'] = model_to_dict(equipment)
                data['Armament'] = model_to_dict(armament)

            elif equipment.type == 'Wearable':
                wearable = models.Model_wearable.objects.get(pk=equipment.type_id)
                data['registred'] = equipment.type
                data['equipment'] = model_to_dict(equipment)
                data['Wearable'] = model_to_dict(wearable)
                

            print(f"Equipamento é um {equipment.type}")

        # if settings.AUX['UID'] != '':
        #     settings.AUX['UID'] = ""
    else:
        data = {
            'uid': '',
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
