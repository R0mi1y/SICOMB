from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .forms import *


# Registra o equipamento
@login_required
def register_equipment(request):
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "equipment/teste.html", {"form": form})
    form = EquipmentForm()  # Se for bem sucedido ele zera o form

    return render(request, "equipment/teste.html", {"form": form})


# valida o uid pra cadastro
def valid_uid(request):
    uid = settings.AUX["UID"]
    settings.AUX["UID"] = ""
    try:
        Equipment.objects.get(uid=uid)
    except Equipment.DoesNotExist:  # se não existe
        return JsonResponse(
            {"uid": uid}
        )  # retorna o uid pq significa que pode cadastrar
    return JsonResponse({"msm": "UID já cadastrado", "uid": ""})


# valida o numero de série pra cadastro
def valid_serial_number(request, sn):
    try:
        Equipment.objects.get(serial_number=sn)
    except Equipment.DoesNotExist:  # se não existe
        return JsonResponse({"exists": False})  # retorna que não existe
    return JsonResponse({"msm": "Numero de série já cadastrado", "exists": True})


def get_equipment_serNum(request, serial_number):
    if serial_number.isdigit():
        try:
            equipment = Equipment.objects.get(serial_number=serial_number)
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"msm": "Equipamento não existe na base de dados!", "registred": False}
            )
        data = {}
        data["equipment"] = model_to_dict(equipment)

        if (
            equipment.armament != None
        ):  # Recupera o objeto armamento, que complementa o equipamento
            data["registred"] = "armament"
            data["model"] = model_to_dict(equipment.armament)

        elif (
            equipment.wearable != None
        ):  # Recupera o objeto vestimento, que complementa o equipamento
            data["registred"] = "wearable"
            data["model"] = model_to_dict(equipment.wearable)

        elif (
            equipment.accessory != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["registred"] = "accessory"
            data["model"] = model_to_dict(equipment.accessory)

        elif (
            equipment.grenada != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["registred"] = "grenada"
            data["model"] = model_to_dict(equipment.grenada)

        return JsonResponse(data)
    else:
        try:
            bullet = Bullet.objects.get(caliber=serial_number)
        except Bullet.DoesNotExist:
            return JsonResponse(
                {"msm": "Munição não existe na base de dados!", "registred": False}
            )
        data = {}
        data["bullet"] = model_to_dict(bullet)

        return JsonResponse(data)


# Retorna o equipamento referente ao uid mais recente em formato JSON
def get_equipment(request):
    data = {"uid": ""}

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        data["registred"] = request.POST.get("type")

        # Caso seja uma munição
        if request.POST.get("type") == "bullet":
            try:
                bullet = Bullet.objects.get(pk=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                settings.AUX["UID"] = ""
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data["equipment"] = model_to_dict(bullet)

    # Para os equipamentos com a tag
    if settings.AUX["UID"] != "":
        data["uid"] = settings.AUX["UID"]

        try:
            equipment = Equipment.objects.get(
                uid=settings.AUX["UID"]
            )  # Recupera o objeto Equipamento
        except Equipment.DoesNotExist:
            settings.AUX["UID"] = ""
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

        data["equipment"] = model_to_dict(equipment)

        if (
            equipment.armament != None
        ):  # Recupera o objeto armamento, que complementa o equipamento
            data["registred"] = "armament"
            data["model"] = model_to_dict(equipment.armament)

        elif (
            equipment.wearable != None
        ):  # Recupera o objeto vestimento, que complementa o equipamento
            data["registred"] = "wearable"
            data["model"] = model_to_dict(equipment.wearable)

        elif (
            equipment.accessory != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["registred"] = "accessory"
            data["model"] = model_to_dict(equipment.accessory)

        elif (
            equipment.grenada != None
        ):  # Recupera o objeto acessorio, que complementa o equipamento
            data["registred"] = "grenada"
            data["model"] = model_to_dict(equipment.grenada)

        settings.AUX["UID"] = ""
    return JsonResponse(data)  # Retorna o dicionário em forma de api


# Recebe o UID do ESP
def set_uid(request):
    # Armazena o UID recebido numa variável global no arquivo settings
    if request.method == "POST":
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.POST.get("uid")
    elif request.method == "GET":
        # TODO Mudar para método POST aqui e no esp
        settings.AUX["UID"] = request.GET.get("uid")

    return render(request, "equipment/set_answer.html", {"uid": settings.AUX["UID"]})


# # Retorna a lista de tipos, modelos e tipos de equipamentos em formato json para a página de registro
# def get_models_equipment(request):
#     armaments = Model_armament.objects.all()
#     armament_models = []

#     for i in armaments:
#         armaments.append(i.model)

#     wearbles = Model_wearable.objects.all()
#     wearbles_models = []

#     for i in wearbles:
#         wearbles.append(i.model)

#     accessory = Model_accessory.objects.all()
#     accessory_models = []

#     for i in accessory:
#         accessory.append(i.model)

#     grenada = Model_grenada.objects.all()
#     grenada_models = []

#     for i in grenada:
#         grenada.append(i.model)

#     bullet = Bullet.objects.all()
#     bullet_models = []

#     for i in bullet:
#         bullet.append(model_to_dict(i))

#     types = {
#         "Munição": {"name": "Munição", "eng_name": "Bullet", "models": bullet_models},
#         "Granada": {"name": "Granada", "eng_name": "Grenada", "models": grenada_models},
#         "Acessório": {
#             "name": "Acessorio",
#             "eng_name": "Acessory",
#             "models": accessory_models,
#         },
#         "Vestível": {
#             "name": "Vestível",
#             "eng_name": "Wearble",
#             "models": wearbles_models,
#         },
#         "Armamento": {
#             "name": "Armamento",
#             "eng_name": "Armament",
#             "models": armament_models,
#         },
#     }

#     return JsonResponse(types)
