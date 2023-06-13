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

list_equipment = {}  # lista de equipamentos
list_equipment_removed = {}  # lista de equipamentos removidos


# cadastra a carga com a lista
@login_required
def confirm_cargo(request):
    policial = RegisterPolice.objects.get(matricula='WA025ALM')
    data = {}
    if request.method == "POST":
        data_hora_atual = datetime.now()  # pega a data atual
        data_hora_futura = data_hora_atual + timedelta(
            hours=6
        )  # TODO: definir carha horária da carga
        cargo = Cargo(expected_cargo_return_date=data_hora_futura)  # Cadastra a carga
        cargo.save()

        # Cadastra a lista de equipamentos na tabela equipment_cargo
        # com a carga cadastrada e os equipamentos da lista
        for key in list_equipment:
            if key.isdigit():
                equipment = Equipment.objects.get(serial_number=key)
                equipment.status = "Indisponível"
                equipment.save()

                Equipment_cargo(
                    cargo=cargo,
                    equipment=equipment,
                    observation=list_equipment[key]["observation"],
                    amount=list_equipment[key]["amount"],
                ).save()
            elif key[0] == ".":  # se for uma munição
                bullet = Bullet.objects.get(caliber=key)
                if int(bullet.amount) - int(list_equipment[key]["amount"]) < 0:
                    list_equipment[key]["amount"] = bullet.amount
                    bullet.amount = 0
                    data["msm"] = "Munição insuficiente, munição zerada"
                else:
                    bullet.amount = int(bullet.amount) - int(
                        list_equipment[key]["amount"]
                    )
                bullet.save()

                Equipment_cargo(
                    cargo=cargo,
                    bullet=bullet,
                    observation=list_equipment[key]["observation"],
                    amount=list_equipment[key]["amount"],
                ).save()

        list_equipment.clear()
        list_equipment_removed.clear()
    
    data['policial'] = policial

    return render(request, "cargo/cargo.html", data)


@login_required
def get_cargo(
    request, id
):  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    cargo = Cargo.objects.get(id=id)
    list = Equipment_cargo.objects.filter(cargo=cargo)

    for key in list:
        print(key.equipment.type)

    return redirect("fazer_carga")


# Cancela a carga e zera as listas
def cancel_cargo(request):
    list_equipment.clear()
    list_equipment_removed.clear()

    return redirect("fazer_carga")


# Retorna a lista
def get_list_equipment(request):
    return JsonResponse(list_equipment)


@csrf_exempt  # tira a necessidade do token csrf
# adiciona um equipamento à lista na views vindo do front
def add_list_equipment(request, serial_number, obs, amount):
    if request.method == "POST":
        if serial_number.isdigit():
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
        list_equipment[serial_number] = data
        list_equipment[serial_number]["observation"] = obs if obs != "-" else ""
        list_equipment[serial_number]["amount"] = amount

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

        list_equipment_removed[
            serial_number
        ] = data  # salva na lista de equipamentos removidos

        del list_equipment[serial_number]  # deleta efetivamente

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})


def get_dashboard_cargas(request):
    json_cargos = []
    cargos = Cargo.objects.all()

    for cont, i in enumerate(cargos):
        equipment_cargo = Equipment_cargo.objects.filter(cargo=i.pk)

        for cont2, y in enumerate(equipment_cargo):
            if y.equipment != None:
                equipment = y.equipment

                if (
                    equipment.armament != None
                ):  # Recupera o objeto armamento, que complementa o equipamento
                    registred = "Armamento"
                    model = equipment.armament

                elif (
                    equipment.wearable != None
                ):  # Recupera o objeto vestimento, que complementa o equipamento
                    registred = "Vestimento"
                    model = equipment.wearable

                elif (
                    equipment.accessory != None
                ):  # Recupera o objeto acessorio, que complementa o equipamento
                    registred = "Acessório"
                    model = equipment.accessory

                elif (
                    equipment.grenada != None
                ):  # Recupera o objeto acessorio, que complementa o equipamento
                    registred = "Granada"
                    model = equipment.grenada

            elif y.bullet:
                registred = "Munição"
                model = y.bullet

                y.registred = model
            else:
                print(
                    "ERROOOOOUUUU ================================================================="
                )

        json_cargos.append([i, equipment_cargo])
    # return JsonResponse(json_cargos)
    return render(request, "cargo/dashboard-cargo.html", {"cargos": json_cargos})
