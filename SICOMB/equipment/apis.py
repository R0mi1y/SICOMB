from django.shortcuts import render
from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
from SICOMB import settings
from load.models import *
from load.apis import require_user_pass
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_user_pass
def get_bullets(request):
    bullets = Bullet.objects.all()
    data = {}
    for i, caliber in enumerate(bullets):
        data[i] = model_to_dict(caliber)
        data[i]['image_path'] = caliber.image_path.url if caliber.image_path else ''

    return JsonResponse(data)


# valida o uid pra cadastro
@csrf_exempt
@require_user_pass
def valid_uid(request):
    if settings.AUX["uids"].__len__() > 0:
        uid = settings.AUX["uids"][settings.AUX["uids"].__len__() - 1]
        settings.AUX["uids"][settings.AUX["uids"].__len__() - 1] = ""
        try:
            Equipment.objects.get(uid=uid)
        except Equipment.DoesNotExist:  # se não existe
            return JsonResponse(
                {"uid": uid}
            )  # retorna o uid pq significa que pode cadastrar
        return JsonResponse({"msm": "UID já cadastrado", "uid": ""})
    else:
        return JsonResponse({"uid": ""})


# valida o numero de série pra cadastro
@csrf_exempt
@require_user_pass
def valid_serial_number(request, sn):
    try:
        Equipment.objects.get(serial_number=sn)
    except Equipment.DoesNotExist:  # se não existe
        return JsonResponse({"exists": False})  # retorna que não existe
    return JsonResponse({"msm": "Numero de série já cadastrado", "exists": True})


@csrf_exempt
@require_user_pass
def get_equipment_serNum(request, serial_number):
    if serial_number.isdigit():
        try:
            equipment = Equipment.objects.get(serial_number=serial_number)
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"msm": "Equipamento não existe na base de dados!", "registred": False}
            )
        data = {
            "equipment": model_to_dict(equipment),
            "registred": equipment.model_type.model.replace("model_", ""),
            "model": model_to_dict(equipment.model),
        }
        data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

        return JsonResponse(data)
    elif not serial_number.isdigit():
        try:
            bullet = Bullet.objects.get(caliber=serial_number)
        except Bullet.DoesNotExist:
            return JsonResponse(
                {
                    "msm": "Munição não existe na base de dados!",
                    "registred": False,
                    "uid": "",
                }
            )
        data = {
            "uid": "Search",
            "model": model_to_dict(bullet),
            "registred": "bullet"
        }
        data['model']['image_path'] = bullet.image_path.url if bullet.image_path else ''
        data["equipment"] = data["model"]

        return JsonResponse(data)


@csrf_exempt
@require_user_pass
def get_equipment_avalible(request):
    """
    Retorna o equipamento referente ao uid mais recente em formato JSON
    Especificamente diferente na questão de que, se ele estiver indisponível 
    ele retorna uma mensagem falando o motivo.
    
    Usado no processo de fetch load
    """
    
    data = {
        "uid": "",
        "confirmCargo": settings.AUX["confirmCargo"],
    }

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        # Caso seja uma munição
        if request.GET.get("type") == "bullet":
            caliber = request.GET.get("pk").replace("%20", " ")
            try:
                bullet = Bullet.objects.get(caliber=caliber)
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado", "a": caliber}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data = {
                "uid": "Search",
                "equipment": model_to_dict(bullet),
                "registred": "bullet",
            }
            data['equipment']['image_path'] = bullet.image_path.url if bullet.image_path else ''
            data['model'] = data['equipment']
        elif request.GET.get("type") == "equipment":
            try:
                equipment = Equipment.objects.get(serial_number=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )
            data = {
                "uid": "Search",
                "equipment": model_to_dict(equipment),
                "registred": equipment.model_type.model.replace("model_", ""),
                "model": model_to_dict(equipment.model),
            }
            data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

    # Para os equipamentos com a tag
    elif len(settings.AUX["uids"]) > 0:
        uid = settings.AUX["uids"].pop()
        data["uid"] = uid

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status != "Disponível":
            return JsonResponse(
                {
                    "uid": "",
                    "msm": "Equipamento não disponível, equipamento em uma carga de "
                    + equipment.status,
                }
            )

        data["equipment"] = model_to_dict(equipment)
        data["registred"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)
        data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

    return JsonResponse(data)  # Retorna o dicionário em forma de api


@csrf_exempt
@require_user_pass
def allow_cargo(request):
    print(settings.AUX["confirmCargo"])
    settings.AUX["confirmCargo"] = True
    print(settings.AUX["confirmCargo"])
    return JsonResponse({})


@csrf_exempt
@require_user_pass
def get_equipment_unvalible(request, id):
    """
    Retorna o equipamento referente ao uid mais recente em formato JSON
    Especificamente diferente na questão de que, se ele estiver disponível 
    ele retorna uma mensagem falando o motivo.
    
    Usado no processo de fetch unload
    """
    
    data = {
        "uid": "",
        "confirmCargo": settings.AUX["confirmCargo"],
    }
    
    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        print(request.GET.get("type"))
        data["registred"] = request.GET.get("type")

        # Caso seja uma munição
        if request.GET.get("type") == "bullet":
            try:
                bullet = Bullet.objects.get(caliber=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
            
            if Equipment_load.objects.filter(load=id, bullet=bullet).exists():
                data["uid"] = 'Search'
                data["equipment"] = model_to_dict(bullet)
                data["equipment"]['image_path'] = bullet.image_path.url if bullet.image_path else ''
                data["model"] = data["equipment"]
            else:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não presente na carga atual."}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

        elif request.GET.get("type") == "equipment":
            try:
                equipment = Equipment.objects.get(serial_number=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )
                
            if Equipment_load.objects.filter(load=id, equipment=equipment).exists():
                data = {
                    "uid": "Search",
                    "equipment": model_to_dict(equipment),
                    "registred": equipment.model_type.model.replace("model_", ""),
                    "model": model_to_dict(equipment.model),
                }
                data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

                return JsonResponse(data)
            else:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não presente na carga atual."}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
                
    # Para os equipamentos com a tag
    elif settings.AUX["uids"].__len__() > 0:
        uid = settings.AUX["uids"].pop()
        data["uid"] = uid

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status == "Disponível":
            return JsonResponse(
                {
                    "uid": "",
                    "msm": "Equipamento não está na carga.",
                }
            )
        for equipment_load in Equipment_load.objects.filter(load=id):
            if equipment == equipment_load.equipment:
                data["equipment"] = model_to_dict(equipment)
                data["registred"] = equipment.model_type.model.replace("model_", "")
                data["model"] = model_to_dict(equipment.model)
                data["model"]['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''
                
                return JsonResponse(data)  # Retorna o dicionário em forma de api
                
        return JsonResponse(
            {"uid": "", "msm": "Equipamento não presente na carga atual."}
        )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
    return JsonResponse(data)  # Retorna o dicionário em forma de api


@csrf_exempt
# @require_user_pass
def set_uid(request):
    """
    Método que recebe o UID do ESP e armazena na memória
    """
    
    data = {"uid": "Não setado"}
    # Armazena o UID recebido num array
    if request.method == "GET":
        if (
            request.GET.get("uid") != ""
            and request.GET.get("uid") != None
            and request.GET.get("uid") not in settings.AUX["uids"]
        ):
            settings.AUX["uids"].append(request.GET.get("uid"))
            data["uid"] = settings.AUX["uids"][settings.AUX["uids"].__len__() - 1]
    print(settings.AUX["uids"])

    return render(request, "equipment/set_answer.html", data)


@csrf_exempt
@require_user_pass
def get_uids(request):
    """
    Returns:
        Array: JSON com todos os uids
    """
    dicionario = dict(enumerate(settings.AUX["uids"]))
    return JsonResponse(dicionario)