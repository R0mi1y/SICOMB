from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from load.models import *
from equipment.models import *
from police.models import *
from django.conf import settings
from django.utils import timezone
from equipment.templatetags.custom_filters import require_user_pass


def convert_date(data_hora_utc):
    # Converter para um objeto de data e hora do Django
    data_hora = timezone.datetime.strptime(data_hora_utc, "%Y-%m-%d %H:%M:%S.%f%z")

    # Converter para o fuso horário brasileiro
    data_hora_brasileira = data_hora.astimezone(timezone.get_current_timezone())

    # Formatar a data e hora no formato desejado
    formato_br = "%d/%m/%Y %H:%M:%S"
    data_hora_formatada = data_hora_brasileira.strftime(formato_br)

    return data_hora_formatada


@csrf_exempt
@require_user_pass
def get_loads_police(request, plate):
    # Filtrar os objetos load com base no campo "police" igual a "plate"
    police = Police.objects.filter(matricula=plate).first()
    loads_filtrados = Load.objects.filter(police=police, 
    status__in=['ATRASADA', 'DENTRO DO PRAZO', 'DATA DE RETORNO NÃO DEFINIDA', 'PARCIALMENTE DESCARREGADA COM ATRASO', 'PARCIALMENTE DESCARREGADA']
)
    
    # Criar uma lista chamada "loads" e preencher com os dicionários dos objetos load filtrados
    loads = []
    for load in loads_filtrados:
        dicionario_load = model_to_dict(load)
        dicionario_load["itens_amount"] = Equipment_load.objects.filter(
            load=load
        ).__len__()
        dicionario_load["date_load"] = convert_date(str(dicionario_load["date_load"]))
        if dicionario_load["expected_load_return_date"]:
            dicionario_load["expected_load_return_date"] = convert_date(
                str(dicionario_load["expected_load_return_date"])
            )

        loads.append(dicionario_load)

    data = {"loads_police": loads}

    return JsonResponse(data)



@csrf_exempt
@require_user_pass
def get_load(
    request, id
):  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    
    tipo_model = {
        'wearable' : 'Vestmento',
        'accessory' : 'Acessório',
        'armament' : 'Armamento',
        'grenada' : 'Granada',
        'bullet' : 'Munição',
    }
    
    load = Load.objects.get(id=id)
    equipment_loads = []
    for load in Equipment_load.objects.filter(load=load, status="Pendente"):
        equipment_load = model_to_dict(load)
        equipment = {}
        if load.equipment:
            equipment["equipment"] = model_to_dict(load.equipment)
            # equipment["registred"] = load.equipment.model_type.model.replace("model_", "")
            equipment["campo"] = tipo_model[load.equipment.model_type.model.replace("model_", "")]
            equipment["model"] = model_to_dict(load.equipment.model)
            equipment["model"]["image_path"] = load.equipment.model.image_path.url if load.equipment.model.image_path else ''
        else:
            equipment["equipment"] = model_to_dict(load.bullet)
            equipment["equipment"]["image_path"] = load.bullet.image_path.url if load.bullet.image_path else ''
            equipment["model"] = equipment["equipment"]
            # equipment["registred"] = "bullet"
            equipment["campo"] = "bullet"
            

        equipment["amount"] = load.amount
        equipment_load["Equipment&model"] = equipment
        equipment_loads.append(equipment_load)

    load = model_to_dict(load)
    load["equipment_loads"] = equipment_loads

    return JsonResponse(load)


# Retorna a lista apenas se não houver nenhum equipamento indisponível nela
@csrf_exempt
@require_user_pass
def get_list_equipment_avalible(request):
    for i in settings.AUX["list_equipment"]:
        print(settings.AUX["list_equipment"][i])
        
        if settings.AUX["list_equipment"][i]["registred"] and settings.AUX["list_equipment"][i]["registred"] != "bullet":
            if Equipment.objects.get(serial_number=i).status.lower() != "disponivel":
                
                settings.AUX["list_equipment"] = {}
    return JsonResponse(settings.AUX["list_equipment"])


# Retorna a lista
@csrf_exempt
@require_user_pass
def get_list_equipment(request):
    return JsonResponse(settings.AUX["list_equipment"])


@csrf_exempt
@require_user_pass
def add_list_equipment(request):
    if request.method == "POST":
        # password = request.POST.get('pass')
        # user = request.POST.get('user')
        obs = request.POST.get('observation')
        serial_number = request.POST.get('serialNumber')
        amount = request.POST.get('amount')
        
        # if Police.objects.filter(username=user, password=password).exists():
        if serial_number.isdigit() or "ac" in serial_number:
            equipment = get_object_or_404(Equipment, serial_number=serial_number)
            data = {
                "equipment": model_to_dict(equipment),
                "model": model_to_dict(equipment.model),
                "registred": equipment.model_type.model.replace("model_", ""),
                "observation": obs if obs != "-" else "",
                "amount": amount,
            }
            
            data["model"]["image_path"] = equipment.model.image_path.url if equipment.model.image_path else ''
            
            settings.AUX["list_equipment"][serial_number] = data
            
        elif not serial_number.isdigit():  # se for uma munição
            bullet = get_object_or_404(Bullet, caliber=serial_number)
            
            if settings.AUX["list_equipment"].get(serial_number) is not None:
                print(settings.AUX["list_equipment"].get('serial_number'))
                settings.AUX["list_equipment"][serial_number]["amount"] += int(amount)
            else:
                data = {
                    "model": model_to_dict(bullet),
                    "campo": "Munição",
                    "observation": obs if obs != "-" else "",
                    "amount": int(amount),
                }
                data["model"]["image_path"] = bullet.image_path.url if bullet.image_path else ''
                data["equipment"] = data["model"]
                settings.AUX["list_equipment"][serial_number] = data
        
        return JsonResponse({"uid": settings.AUX["list_equipment"]})
        # else:
        #     return JsonResponse({"message": "Credenciais inválidas"})
    else:
        return JsonResponse({"message": "Método HTTP não suportado"})


# Remove da lista de equipamentos
@csrf_exempt
@require_user_pass
def remove_list_equipment(request):
    if request.method == "POST":
        serial_number = request.POST.get('serial_number')
        obs = request.POST.get('obs')
        settings.AUX["list_equipment_removed"][serial_number] = settings.AUX[
            "list_equipment"
        ][serial_number]
        
        settings.AUX["list_equipment_removed"][serial_number]["observation"] = obs if obs != "-" else ""
        del settings.AUX["list_equipment"][serial_number]  # deleta efetivamente

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})

