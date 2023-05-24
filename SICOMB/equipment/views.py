from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from . import models
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

@login_required
def register_equipment(request):
    
    if request.method == 'POST':
        models.Equipment(
            serial_number=request.POST.get('serial_number'),
            uid=request.POST.get('uid'),
            type=request.POST.get('type'),
            type_id=request.POST.get('type_id'),
        ).save()
        print('Chegou aqui')
        return render(request, 'equipment/register-equipment.html', {'message': 'Equipamento cadastrado com sucesso'})
    else:
        return render(request, 'equipment/register-equipment.html')

# Retorna o UID mais recente em formato JSON


@login_required
def get_equipment(request):
    data = {}
    
    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get('type') != None:
        data['registred'] = request.POST.get('type')
        
        # Caso seja uma granada
        if request.POST.get('type') == 'grenada':
            try:
                grenada = models.Grenada.objects.get(pk=request.GET.get('id'))
            except models.Equipment.DoesNotExist:
                return JsonResponse({'uid': '', 'msm':'Equipamento não cadastrado'}) # Caso o equipamento não esteja cadastrado ele simplismente ignora
            
            data['grenada'] = model_to_dict(grenada)

        # Caso seja uma munição
        if request.POST.get('type') == 'bullet':
            try:
                bullet = models.Bullet.objects.get(pk=request.GET.get('pk'))
            except models.Equipment.DoesNotExist:
                return JsonResponse({'uid': '', 'msm':'Equipamento não cadastrado'}) # Caso o equipamento não esteja cadastrado ele simplismente ignora
            
            data['equipment'] = model_to_dict(bullet)
    
    # Para os equipamentos com a tag
    if settings.AUX['UID'] != '':
        data['uid'] = settings.AUX['UID']
        
        try:
            equipment = models.Equipment.objects.get(
                uid=settings.AUX['UID'])  # Recupera o objeto Equipamento
        except models.Equipment.DoesNotExist:
            return JsonResponse({'uid': '', 'msm':'Equipamento não cadastrado'}) # Caso o equipamento não esteja cadastrado ele simplismente ignora
            
        else:
            data['registred'] = equipment.type
            data['equipment'] = model_to_dict(equipment)
            
            if equipment.armament != None: # Recupera o objeto armamento, que complementa o equipamento
                data['Armament'] = model_to_dict(equipment.armament)

            elif equipment.wearable != None: # Recupera o objeto vestimento, que complementa o equipamento
                data['Wearable'] = model_to_dict(equipment.wearable)
            
            elif equipment.accessory != None: # Recupera o objeto acessorio, que complementa o equipamento
                data['accessory'] = model_to_dict(equipment.accessory)
        
    return JsonResponse(data) # Retorna o dicionário em forma de api
        

    #     armament = models.Armament.objects.all()
    #     wearable = models.Wearable.objects.all()

    #     set_armament = {}
    #     set_wearable = {}

    #     for i in armament:
    #         set_armament['armamento ' + str(i.pk)] = model_to_dict(i)
    #     for i in wearable:
    #         set_wearable['vestivel ' + str(i.pk)] = model_to_dict(i)

    #     data = {
    #         'uid': settings.AUX['UID'],
    #         'registred': False,
    #         'Armament': '',
    #         'Wearable': '',
    #     }

    #     if equipment is None:
    #         data['Armament'] = set_armament
    #         data['Wearable'] = set_wearable

    #         print(str(data) + " Equipamento não cadastrado")
    #     elif equipment.type == 'Armament':
    #         armament = models.Armament.objects.get(pk=equipment.type_id)
    #         data['registred'] = equipment.type
    #         data['equipment'] = model_to_dict(equipment)
    #         data['Armament'] = model_to_dict(armament)

    #         print("Equipamento é um armamento")
    #     elif equipment.type == 'Wearable':
    #         wearable = models.Wearable.objects.get(pk=equipment.type_id)
    #         data['registred'] = equipment.type
    #         data['equipment'] = model_to_dict(equipment)
    #         data['Wearable'] = model_to_dict(wearable)

    #         print("Equipamento é um vestível")

    #     if settings.AUX['UID'] != '':
    #         settings.AUX['UID'] = ""
    # else:
    #     data = {
    #         'uid': settings.AUX['UID'],
    #         'registred': True,
    #     }

    #     print("uid não inserido")
    # return JsonResponse(data)


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
