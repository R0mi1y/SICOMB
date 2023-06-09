from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cargo.models import *
from equipment.models import *
from datetime import datetime, timedelta

list_equipment = {}
list_equipment_removed = {}


# Create your views here.
def confirm_cargo(request):
    data_hora_atual = datetime.now()
    data_hora_futura = data_hora_atual + timedelta(hours=6)
    cargo = Cargo(expected_cargo_return_date=data_hora_futura)
    cargo.save()

    for key in list_equipment:
        Equipment_cargo(
            cargo=cargo, equipment=Equipment.objects.get(serial_number=key)
        ).save()

    list_equipment.clear()
    list_equipment_removed.clear()

    return redirect("register_equipment")


@login_required
def redirect_cargo(request):
    return render(request, "equipment/fazer_carga.html")


@login_required
def get_cargo(request, id):
    cargo = Cargo.objects.get(id=id)
    list = Equipment_cargo.objects.filter(cargo=cargo)

    for key in list:
        print(key.equipment.type)

    return redirect("fazer_carga")


def cancel_cargo(request):
    list_equipment.clear()
    list_equipment_removed.clear()

    return redirect("register_equipment")


def get_list_equipment(request):
    return JsonResponse(list_equipment)


@csrf_exempt
def add_list_equipment(request, serial_number, obs):
    if request.method == "POST":
        equipment = Equipment.objects.get(serial_number=serial_number)
        equipment.observation = obs
        data = {
            "equipment": model_to_dict(equipment),
        }

        if (
            equipment.armament != None
        ):  # Recupera o objeto armamento, que complementa o equipamento
            data["model"] = model_to_dict(equipment.armament)
            data["campo"] = "Armamento"

        elif (
            equipment.wearable != None
        ):  # Recupera o objeto vestimento, que complementa o equipamento
            data["model"] = model_to_dict(equipment.wearable)
            data["campo"] = "Vestível"

        elif (
            equipment.accessory != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["model"] = model_to_dict(equipment.accessory)
            data["campo"] = "Acessório"

        elif (
            equipment.grenada != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["model"] = model_to_dict(equipment.grenada)
            data["campo"] = "Granada"

        # equipment.save()
        list_equipment[serial_number] = data

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})


@csrf_exempt
def remove_list_equipment(request, serial_number, obs):
    if request.method == "POST":
        equipment = Equipment.objects.get(serial_number=serial_number)
        equipment.observation = obs
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

        equipment.save()
        list_equipment_removed[serial_number] = data

        del list_equipment[serial_number]
        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})
