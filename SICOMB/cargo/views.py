import pprint
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cargo.models import *
from equipment.models import *
from police.models import *
from datetime import datetime, timedelta
import json
from django.conf import settings
from django.utils import timezone


settings.AUX['list_equipment'] = {}  # lista de equipamentos
settings.AUX['list_equipment_removed'] = {}  # lista de equipamentos removidos


# cadastra a carga com a lista
@login_required
def confirm_cargo(request):
    data = {}
    police = None
    if request.method == "POST":
        turn_type = request.POST.get("turn_type")
        data_hora_atual = datetime.now()  # pega a data atual
        
        if turn_type == "6H" or turn_type == "12H" or turn_type == "24H":
            turn_type = turn_type.replace("H", "")
            
            data_hora_futura = data_hora_atual + timedelta(
                hours=int(turn_type)
            )
        else:
            data_hora_futura = None
            
        try:
            police = RegisterPolice.objects.get(matricula=request.POST.get("plate"))
        except:
            pass
        
        cargo = Cargo(expected_cargo_return_date=data_hora_futura, turn_type=turn_type, police=police)  # Cadastra a carga
        cargo.save()

        # Cadastra a lista de equipamentos na tabela equipment_cargo
        # com a carga cadastrada e os equipamentos da lista
        for key in settings.AUX['list_equipment']:
            if key.isdigit():
                equipment = Equipment.objects.get(serial_number=key)
                equipment.status = turn_type
                equipment.save()

                Equipment_cargo(
                    cargo=cargo,
                    equipment=equipment,
                    observation=settings.AUX['list_equipment'][key]["observation"],
                    amount=settings.AUX['list_equipment'][key]["amount"],
                ).save()
        for key in settings.AUX['list_equipment_removed']:
            if key.isdigit():
                equipment = Equipment.objects.get(serial_number=key)
                equipment.status = turn_type
                equipment.save()

                Equipment_cargo(
                    cargo=cargo,
                    equipment=equipment,
                    observation=settings.AUX['list_equipment_removed'][key]["observation"],
                    amount=settings.AUX['list_equipment_removed'][key]["amount"],
                    status='Retornado'
                ).save()
            elif key[0] == ".":  # se for uma munição
                bullet = Bullet.objects.get(caliber=key)
                if int(bullet.amount) - int(settings.AUX['list_equipment'][key]["amount"]) < 0:
                    settings.AUX['list_equipment'][key]["amount"] = bullet.amount
                    bullet.amount = 0
                    data["msm"] = "Munição insuficiente, munição zerada"
                else:
                    bullet.amount = int(bullet.amount) - int(
                        settings.AUX['list_equipment'][key]["amount"]
                    )
                bullet.save()

                Equipment_cargo(
                    cargo=cargo,
                    bullet=bullet,
                    observation=settings.AUX['list_equipment'][key]["observation"],
                    amount=settings.AUX['list_equipment'][key]["amount"],
                ).save()
                
        settings.AUX["matricula"] = ''

        settings.AUX['list_equipment'].clear()
        settings.AUX['list_equipment_removed'].clear()

    data["policial"] = police

    return render(request, "cargo/cargo_temporary.html", data)


def convert_date(data_hora_utc):
    # Converter para um objeto de data e hora do Django
    data_hora = timezone.datetime.strptime(data_hora_utc, "%Y-%m-%d %H:%M:%S.%f%z")

    # Converter para o fuso horário brasileiro
    data_hora_brasileira = data_hora.astimezone(timezone.get_current_timezone())

    # Formatar a data e hora no formato desejado
    formato_br = "%d/%m/%Y %H:%M:%S"
    data_hora_formatada = data_hora_brasileira.strftime(formato_br)

    return data_hora_formatada



def get_cargos_police(request, plate):
    # Filtrar os objetos Cargo com base no campo "police" igual a "plate"
    cargos_filtrados = Cargo.objects.filter(police=plate, status="Pendente")

    # Criar uma lista chamada "cargos" e preencher com os dicionários dos objetos Cargo filtrados
    cargos = []
    for cargo in cargos_filtrados:
        dicionario_cargo = model_to_dict(cargo)
        dicionario_cargo['itens_amount'] = Equipment_cargo.objects.filter(cargo=cargo).__len__()
        dicionario_cargo['date_cargo'] = convert_date(str(dicionario_cargo['date_cargo']))
        if dicionario_cargo['expected_cargo_return_date']:
            dicionario_cargo['expected_cargo_return_date'] = convert_date(str(dicionario_cargo['expected_cargo_return_date']))
        
        cargos.append(dicionario_cargo)
        
    data = {'cargos_police' : cargos}
    
    return JsonResponse(data)
    
    
# @login_required
def get_cargo(request, id):  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    cargo = Cargo.objects.get(id=id)
    equipment_cargos = []
    for cargo in Equipment_cargo.objects.filter(cargo=cargo):
        equipment_cargo = model_to_dict(cargo)
        equipment = {}
        equipment['equipment'] = model_to_dict(cargo.equipment)
        
        if cargo.equipment.armament != None:  # Recupera o objeto armamento, que complementa o equipamento
            equipment["registred"] = "armament"
            equipment["model"] = model_to_dict(cargo.equipment.armament)

        elif cargo.equipment.wearable != None:  # Recupera o objeto vestimento, que complementa o equipamento
            equipment["registred"] = "wearable"
            equipment["model"] = model_to_dict(cargo.equipment.wearable)

        elif cargo.equipment.accessory != None:  # Recupera o objeto acessorio, que complementa o equipamento
            equipment["registred"] = "accessory"
            equipment["model"] = model_to_dict(cargo.equipment.accessory)

        elif cargo.equipment.grenada != None:  # Recupera o objeto acessorio, que complementa o equipamento
            equipment["registred"] = "grenada"
            equipment["model"] = model_to_dict(cargo.equipment.grenada)
        
        equipment['amount'] = cargo.amount
        equipment_cargo['Equipment&model'] = equipment
        equipment_cargos.append(equipment_cargo)
        
    cargo = model_to_dict(cargo)
    cargo['equipment_cargos'] = equipment_cargos
    
    return JsonResponse(cargo)

# Cancela a carga e zera as listas
def cancel_cargo(request):
    settings.AUX['list_equipment'].clear()
    settings.AUX['list_equipment_removed'].clear()

    return redirect("fazer_carga")


# Retorna a lista
def get_list_equipment(request):
    return JsonResponse(settings.AUX['list_equipment'])


@csrf_exempt  # tira a necessidade do token csrf
# adiciona um equipamento à lista na views vindo do front
def add_list_equipment(request, serial_number, obs, amount):
    if request.method == "POST":
        if serial_number == "turn_type":
            settings.AUX['list_equipment']["turn_type"] = obs
        elif serial_number.isdigit():
            equipment = Equipment.objects.get(
                serial_number=serial_number
            )  # Recupera o equipment pelo numero de série
            data = {
                "equipment": model_to_dict(equipment),  # Transforma em um dicionario
            }

            if (
                equipment.armament != None
            ):  # Recupera o modelo armamento, que complementa o equipamento
                data["model"] = model_to_dict(equipment.armament)
                data["campo"] = "Armamento"

            elif (
                equipment.wearable != None
            ):  # Recupera o modelo vestimento, que complementa o equipamento
                data["model"] = model_to_dict(equipment.wearable)
                data["campo"] = "Vestimento"

            elif (
                equipment.accessory != None
            ):  # Recupera o modelo acessorio, que complementa o equipamento
                data["model"] = model_to_dict(equipment.accessory)
                data["campo"] = "Acessório"

            elif (
                equipment.grenada != None
            ):  # Recupera o modelo acessorio, que complementa o equipamento
                data["model"] = model_to_dict(equipment.grenada)
                data["campo"] = "Granada"

            # Adiciona na lista de equipamentos efetivamente
            settings.AUX['list_equipment'][serial_number] = data
            settings.AUX['list_equipment'][serial_number]["observation"] = obs if obs != "-" else ""
            settings.AUX['list_equipment'][serial_number]["amount"] = amount
        elif serial_number[0] == ".":  # se for uma munição
            try:
                bullet = Bullet.objects.get(caliber=serial_number)
            except Bullet.DoesNotExist:
                return JsonResponse(
                    {"msm": "Munição não existe na base de dados!", "registred": False}
                )
            data = {}
            data["model"] = model_to_dict(bullet)
            data["equipment"] = model_to_dict(bullet)
            data["campo"] = "Munição"

            # Adiciona na lista de equipamentos efetivamente
            settings.AUX['list_equipment'][serial_number] = data
            settings.AUX['list_equipment'][serial_number]["observation"] = obs if obs != "-" else ""
            settings.AUX['list_equipment'][serial_number]["amount"] = amount

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})


@csrf_exempt
# Remove da lista de equipamentos
def remove_list_equipment(request, serial_number, obs, amount):
    if request.method == "POST":
        if serial_number.isdigit():
            equipment = Equipment.objects.get(serial_number=serial_number)
            data = {
                "equipment": model_to_dict(equipment),
            }

            if (
                equipment.armament != None
            ):  # Recupera o objeto armamento, que complementa o equipamento
                data["model"] = model_to_dict(equipment.armament)

            elif (
                equipment.wearable != None
            ):  # Recupera o objeto vestimento, que complementa o equipamento
                data["model"] = model_to_dict(equipment.wearable)

            elif (
                equipment.accessory != None
            ):  # Recupera o objeto acessorio, que complementa o equipamento
                data["model"] = model_to_dict(equipment.accessory)

            elif (
                equipment.grenada != None
            ):  # Recupera o objeto acessorio, que complementa o equipamento
                data["model"] = model_to_dict(equipment.grenada)

            equipment.save()  # Salva a observação

        elif serial_number[0] == ".":  # se for uma munição
            try:
                bullet = Bullet.objects.get(caliber=serial_number)
            except Bullet.DoesNotExist:
                return JsonResponse(
                    {"msm": "Munição não existe na base de dados!", "registred": False}
                )
            data = {}
            data["model"] = model_to_dict(bullet)
            data["equipment"] = model_to_dict(bullet)
            data["campo"] = "Munição"
        data[serial_number]["observation"] = obs
        data[serial_number]["amount"] = amount

        settings.AUX['list_equipment_removed'][
            serial_number
        ] = data  # salva na lista de equipamentos removidos

        del settings.AUX['list_equipment'][serial_number]  # deleta efetivamente

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})


def get_dashboard_cargas(request):
    cargos = Cargo.objects.all()
    cargos_aux = []
    qnt = []
    for i in cargos:
        ec = Equipment_cargo.objects.filter(cargo=i)
        cargos_aux.append([i, ec.__len__])

    # return JsonResponse(json_cargos)
    return render(
        request, "cargo/dashboard-cargo.html", {"cargos": cargos_aux, "": qnt}
    )
