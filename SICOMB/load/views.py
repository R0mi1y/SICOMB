from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from load.models import *
from equipment.models import *
from police.models import *
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone


settings.AUX["list_equipment"] = {}  # lista de equipamentos
settings.AUX["list_equipment_removed"] = {}  # lista de equipamentos removidos


# cadastra a carga com a lista
@login_required
def confirm_load(request):
    data = {}
    police = None
    if request.method == "POST":
        if len(settings.AUX["list_equipment"]) > 0 or len(settings.AUX["list_equipment_removed"] > 0):
            turn_type = request.POST.get("turn_type")
            data_hora_atual = datetime.now()  # pega a data atual

            if turn_type == "6H" or turn_type == "12H" or turn_type == "24H":
                data_hora_futura = data_hora_atual + timedelta(
                    hours=int(turn_type.replace("H", ""))
                )
            else:
                data_hora_futura = None

            try:
                police = RegisterPolice.objects.get(matricula=request.POST.get("plate"))
            except:
                pass

            load = Load(
                expected_load_return_date=data_hora_futura,
                turn_type=turn_type,
                police=police,
            )  # Cadastra a carga
            load.save()

            print(settings.AUX["list_equipment"])
            # Cadastra a lista de equipamentos na tabela equipment_load
            # com a carga cadastrada e os equipamentos da lista
            for key in settings.AUX["list_equipment"]:
                if key.isdigit() or "ac" in key:
                    equipment = Equipment.objects.get(serial_number=key)
                    equipment.status = turn_type
                    equipment.save()

                    Equipment_load(
                        load=load,
                        equipment=equipment,
                        observation=settings.AUX["list_equipment"][key]["observation"],
                        amount=settings.AUX["list_equipment"][key]["amount"],
                    ).save()
                elif key[0] == ".":  # se for uma munição
                    print("\n\né uma munição\n\n")
                    bullet = Bullet.objects.get(caliber=key)
                    if (
                        int(bullet.amount)
                        - int(settings.AUX["list_equipment"][key]["amount"])
                        < 0
                    ):
                        settings.AUX["list_equipment"][key]["amount"] = bullet.amount
                        bullet.amount = 0
                        data["msm"] = "Munição insuficiente, munição zerada"
                    else:
                        bullet.amount = int(bullet.amount) - int(
                            settings.AUX["list_equipment"][key]["amount"]
                        )
                    bullet.save()

                    Equipment_load(
                        load=load,
                        bullet=bullet,
                        observation=settings.AUX["list_equipment"][key]["observation"],
                        amount=settings.AUX["list_equipment"][key]["amount"],
                    ).save()

            print(settings.AUX["list_equipment_removed"])

            for key in settings.AUX["list_equipment_removed"]:
                if key.isdigit() or "ac" in key:
                    equipment = Equipment.objects.get(serial_number=key)
                    equipment.status = turn_type
                    equipment.save()

                    Equipment_load(
                        load=load,
                        equipment=equipment,
                        observation=settings.AUX["list_equipment_removed"][key][
                            "observation"
                        ],
                        amount=settings.AUX["list_equipment_removed"][key]["amount"],
                        status="Retornado",
                    ).save()
                elif key[0] == ".":  # se for uma munição
                    print("é uma munição\n")
                    bullet = Bullet.objects.get(caliber=key)

                    Equipment_load(
                        load=load,
                        bullet=bullet,
                        observation=settings.AUX["list_equipment_removed"][key]["observation"],
                        amount=settings.AUX["list_equipment_removed"][key]["amount"],
                        status="Retornado",
                    ).save()

            settings.AUX["matricula"] = ""

            settings.AUX["list_equipment"].clear()
            settings.AUX["list_equipment_removed"].clear()

        data["policial"] = police

    return render(request, "load/load.html", data)


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
    loads_filtrados = Load.objects.filter(police=plate, status="Pendente")

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


# @login_required
def get_load(
    request, id
):  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    load = Load.objects.get(id=id)
    equipment_loads = []
    for load in Equipment_load.objects.filter(load=load):
        equipment_load = model_to_dict(load)
        equipment = {}
        equipment["equipment"] = model_to_dict(load.equipment)

        if (
            load.equipment.armament != None
        ):  # Recupera o objeto armamento, que complementa o equipamento
            equipment["registred"] = "armament"
            equipment["model"] = model_to_dict(load.equipment.armament)

        elif (
            load.equipment.wearable != None
        ):  # Recupera o objeto vestimento, que complementa o equipamento
            equipment["registred"] = "wearable"
            equipment["model"] = model_to_dict(load.equipment.wearable)

        elif (
            load.equipment.accessory != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            equipment["registred"] = "accessory"
            equipment["model"] = model_to_dict(load.equipment.accessory)

        elif (
            load.equipment.grenada != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            equipment["registred"] = "grenada"
            equipment["model"] = model_to_dict(load.equipment.grenada)

        equipment["amount"] = load.amount
        equipment_load["Equipment&model"] = equipment
        equipment_loads.append(equipment_load)

    load = model_to_dict(load)
    load["equipment_loads"] = equipment_loads

    return JsonResponse(load)


# Cancela a carga e zera as listas
def cancel_load(request):
    settings.AUX["list_equipment"].clear()
    settings.AUX["list_equipment_removed"].clear()

    return redirect("fazer_carga")


# Retorna a lista
def get_list_equipment(request):
    print("list_equipment = ||| = " + str(settings.AUX["list_equipment"]) + "\n\n\n")
    print(
        "list_equipment_removed = ||| = " + str(settings.AUX["list_equipment_removed"])
    )
    return JsonResponse(settings.AUX["list_equipment"])


@csrf_exempt  # tira a necessidade do token csrf
# adiciona um equipamento à lista na views vindo do front
def add_list_equipment(request, serial_number, obs, amount):
    if request.method == "POST":
        if serial_number == "turn_type":
            settings.AUX["list_equipment"]["turn_type"] = obs
        elif serial_number.isdigit() or "ac" in serial_number:
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
            settings.AUX["list_equipment"][serial_number] = data
            settings.AUX["list_equipment"][serial_number]["observation"] = (
                obs if obs != "-" else ""
            )
            settings.AUX["list_equipment"][serial_number]["amount"] = amount
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
            settings.AUX["list_equipment"][serial_number] = data
            settings.AUX["list_equipment"][serial_number]["observation"] = (
                obs if obs != "-" else ""
            )
            settings.AUX["list_equipment"][serial_number]["amount"] = amount

        return JsonResponse({"sucesso": "sucesso"})
    else:
        return JsonResponse({"falha": "falha"})


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


def get_dashboard_loads(request):
    loads = Load.objects.all()
    loads_aux = []
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        loads_aux.append([i, ec.__len__])

    # return JsonResponse(json_loads)
    return render(request, "load/dashboard-load.html", {"loads": loads_aux})
