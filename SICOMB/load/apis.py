from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from load.models import *
from equipment.models import *
from police.models import *
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone


def convert_date(data_hora_utc):
    # Converter para um objeto de data e hora do Django
    data_hora = timezone.datetime.strptime(data_hora_utc, "%Y-%m-%d %H:%M:%S.%f%z")

    # Converter para o fuso horário brasileiro
    data_hora_brasileira = data_hora.astimezone(timezone.get_current_timezone())

    # Formatar a data e hora no formato desejado
    formato_br = "%d/%m/%Y %H:%M:%S"
    data_hora_formatada = data_hora_brasileira.strftime(formato_br)

    return data_hora_formatada


def get_loads_police(request, plate):
    # Filtrar os objetos load com base no campo "police" igual a "plate"
    police = Police.objects.filter(matricula=plate).first()
    loads_filtrados = Load.objects.filter(police=police, status="Pendente")
    
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

        # if timezone.now() > dicionario_load["expected_load_return_date"]:
        #     load.status = 'ATRASADA'
        # elif timezone.now() < dicionario_load["expected_load_return_date"]:
        #     load.status = 'DENTRO DO PRAZO'
        # else:
        #     load.status = 'DESCARREGADA'
        
        loads.append(dicionario_load)

    data = {"loads_police": loads}

    return JsonResponse(data)



# @login_required
def get_load(
    request, id
):  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    load = Load.objects.get(id=id)
    equipment_loads = []
    for load in Equipment_load.objects.filter(load=load):
        equipment_load = model_to_dict(load)
        equipment = {}
        if load.equipment:
            equipment["equipment"] = model_to_dict(load.equipment)
            equipment["registred"] = load.equipment.model_type.model.replace("model_", "")
            equipment["model"] = model_to_dict(load.equipment.model)
            equipment["model"]["image_path"] = load.equipment.model.image_path.url if load.equipment.model.image_path else ''
        else:
            equipment["equipment"] = model_to_dict(load.bullet)
            equipment["equipment"]["image_path"] = load.bullet.image_path.url if load.bullet.image_path else ''
            equipment["model"] = equipment["equipment"]
            equipment["registred"] = "bullet"
            

        equipment["amount"] = load.amount
        equipment_load["Equipment&model"] = equipment
        equipment_loads.append(equipment_load)

    load = model_to_dict(load)
    load["equipment_loads"] = equipment_loads

    return JsonResponse(load)


# Retorna a lista
def get_list_equipment(request):
    return JsonResponse(settings.AUX["list_equipment"])


@csrf_exempt # Use o CSRF apenas se necessário
def add_list_equipment(request, serial_number, obs, amount, user, password):
    password = password.replace("%21%", "/")
    
    print(f"Adding Equipment ==---=<{user}> ")
    if request.method == "POST":
        if Police.objects.filter(username=user, password=password).first is not None:
            if serial_number == "turn_type":
                settings.AUX["list_equipment"]["turn_type"] = obs
            elif serial_number.isdigit() or "ac" in serial_number:
                equipment = get_object_or_404(Equipment, serial_number=serial_number)
                data = {
                    "equipment": model_to_dict(equipment),
                    "model": model_to_dict(equipment.model),
                    "registred": equipment.model_type.model.replace("model_", ""),
                    "observation": obs if obs != "-" else "",
                    "amount": amount,
                }
                
                data["model"]["image_path"] = equipment.model.image_path.url if equipment.model.image_path else ''
                
                print(data)
                
                settings.AUX["list_equipment"][serial_number] = data
            elif serial_number[0] == ".":  # se for uma munição
                bullet = get_object_or_404(Bullet, caliber=serial_number)
                data = {
                    "model": model_to_dict(bullet),
                    "campo": "Munição",
                    "observation": obs if obs != "-" else "",
                    "amount": amount,
                }
                data["model"]["image_path"] = bullet.image_path.url if bullet.image_path else ''
                data["equipment"] = data["model"]
                settings.AUX["list_equipment"][serial_number] = data

            return JsonResponse({"message": settings.AUX["list_equipment"]})
        else:
            return JsonResponse({"message": "Credenciais inválidas"})
    else:
        return JsonResponse({"message": "Método HTTP não suportado"})


# Remove da lista de equipamentos
@csrf_exempt
def remove_list_equipment(request, serial_number, obs, amount):
    print(settings.AUX["list_equipment"][serial_number])
    if request.method == "POST":
        settings.AUX["list_equipment_removed"][serial_number] = settings.AUX[
            "list_equipment"
        ][serial_number]
        del settings.AUX["list_equipment"][serial_number]  # deleta efetivamente

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})