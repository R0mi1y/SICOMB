import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .forms import *

uids = []

# Registra o equipamento
@login_required
def delete_equipment(request, id):
    try:
        Equipment.objects.get(pk=id).delete()
    except Equipment.DoesNotExist:
        pass
        
    return redirect("manage_equipment")

@login_required
def register_edit_equipment(request, id=None):
    equipment = None
    if id:
        equipment = Equipment.objects.get(pk=id)
    
    if request.method == "POST":
        if request.POST.get("bullet") and request.POST.get("amount"):
            try:
                bullet = Bullet.objects.get(id=request.POST.get("bullet"))
            except Bullet.DoesNotExist:
                form = EquipmentForm()  # Se for bem sucedido ele zera o form

                return render(
                    request,
                    "equipment/register-equipment.html",
                    {"msm": "Munição não existe na base de dados!", "form": form},
                )
            bullet.amount = int(bullet.amount) + int(request.POST.get("amount"))
            bullet.save()
        else:
            form = EquipmentForm(request.POST, instance=equipment)
            if form.is_valid():
                form.save()
            else:
                return render(request, "equipment/register-equipment.html", {"form": form})
    form = EquipmentForm(instance=equipment)  # Se for bem sucedido ele zera o form

    return render(request, "equipment/register-equipment.html", {"form": form})


@login_required
def register_edit_model(request, model_name=None, id=None):
    model = None
    if model_name:
        if model_name == 'armament':
            if id:
                try:
                    model = Model_armament.objects.get(id=id)
                except Model_armament.DoesNotExist:
                    form = Model_armamentForm()
            form = Model_armamentForm(instance=model)
            
            if request.method == "POST":
                form = Model_armamentForm(request.POST, request.FILES)
                
                if form.is_valid():
                    form.save()
                    
                    return redirect("manage_model")
            return render(request, "equipment/form-model.html", {"form": form, "model": model_name})
                
        elif model_name == 'accessory':
            if id:
                try:
                    model = Model_accessory.objects.get(id=id)
                except Model_accessory.DoesNotExist:
                    form = Model_accessoryForm()
            form = Model_accessoryForm(instance=model)
            
            if request.method == "POST":
                form = Model_accessoryForm(request.POST, request.FILES)
                
                if form.is_valid():
                    form.save()
                    
                    return redirect("manage_model")
            return render(request, "equipment/form-model.html", {"form": form, "model": model_name})
                
        elif model_name == 'wearable':
            if id:
                try:
                    model = Model_wearable.objects.get(id=id)
                except Model_wearable.DoesNotExist:
                    form = Model_wearableForm()
            form = Model_wearableForm(instance=model)
            
            if request.method == "POST":
                form = Model_wearableForm(request.POST, request.FILES)
                
                if form.is_valid():
                    form.save()
                    
                    return redirect("manage_model")
            return render(request, "equipment/form-model.html", {"form": form, "model": model_name})
                
        elif model_name == 'grenada':
            if id:
                try:
                    model = Model_grenada.objects.get(id=id)
                except Model_grenada.DoesNotExist:
                    form = Model_grenadaForm()
            form = Model_grenadaForm(instance=model)
            
            if request.method == "POST":
                form = Model_grenadaForm(request.POST, request.FILES)
                
                if form.is_valid():
                    form.save()
                    
                    return redirect("manage_model")
            return render(request, "equipment/form-model.html", {"form": form, "model": model_name})
        
        elif model_name == 'bullet':
            if id:
                try:
                    model = Bullet.objects.get(id=id)
                except Bullet.DoesNotExist:
                    form = BulletForm()
                    
            form = BulletForm(instance=model)
            
            if request.method == "POST":
                form = BulletForm(request.POST, request.FILES)
                
                if form.is_valid():
                    form.save()
                    
                    return redirect("manage_model")
            return render(request, "equipment/form-model.html", {"form": form, "model": model_name})
                
    return render(request, "equipment/form-model.html", {"form": None})
    
    
def get_bullets(request):
    bullets = Bullet.objects.all()
    data = {}
    for i, caliber in enumerate(bullets):
        data[i] = model_to_dict(caliber)
        
    return JsonResponse(data)


# valida o uid pra cadastro
def valid_uid(request):
    if(uids.__len__() > 0):
        uid = uids[uids.__len__() - 1]
        uids[uids.__len__() - 1] = ""
        try:
            Equipment.objects.get(uid=uid)
        except Equipment.DoesNotExist:  # se não existe
            return JsonResponse(
                {"uid": uid}
            )  # retorna o uid pq significa que pode cadastrar
        return JsonResponse({"msm": "UID já cadastrado", "uid": ""})
    else:
        return JsonResponse({"uid": ''})
    


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
        data["registred"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)

        return JsonResponse(data)
    elif serial_number[0] == ".":
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
        data = {}
        data["model"] = model_to_dict(bullet)
        data["equipment"] = model_to_dict(bullet)
        data["registred"] = "bullet"

        return JsonResponse(data)


# Retorna o equipamento referente ao uid mais recente em formato JSON
def get_equipment_avalible(request):
    data = {"uid": ""}

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        data["registred"] = request.GET.get("type")

        # Caso seja uma munição
        if request.GET.get("type") == "bullet":
            try:
                bullet = Bullet.objects.get(pk=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data["equipment"] = model_to_dict(bullet)

    # Para os equipamentos com a tag
    if uids.__len__() > 0 and uids[uids.__len__() - 1]:
        uid = uids[uids.__len__() - 1]
        uids.pop()
        data["uid"] = uid

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status != "Disponível":
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não disponível, equipamento em uma carga de " + equipment.status}
            )

        data["equipment"] = model_to_dict(equipment)
        data["registred"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)

    return JsonResponse(data)  # Retorna o dicionário em forma de api


# Retorna o equipamento referente ao uid mais recente em formato JSON
def get_equipment_unvalible(request):
    print("Chegou em get_equipment_unvalible()")
    data = {"uid": ""}

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        data["registred"] = request.GET.get("type")

        # Caso seja uma munição
        if request.GET.get("type") == "bullet":
            try:
                bullet = Bullet.objects.get(pk=request.GET.get("pk"))
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data["equipment"] = model_to_dict(bullet)

    # Para os equipamentos com a tag
    if uids.__len__() > 0 and uids[uids.__len__() - 1]:
        uid = uids[uids.__len__() - 1]
        uids.pop()
        data["uid"] = uid

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status == "Disponível":
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não disponível, equipamento não está na carga."}
            )

        data["equipment"] = model_to_dict(equipment)
        data["registred"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)
        
    return JsonResponse(data)  # Retorna o dicionário em forma de api


# Recebe o UID do ESP
def set_uid(request):
    data = {"uid": "Não setado"}
    # Armazena o UID recebido num array
    if request.method == "GET":
        print (request.GET.get("uid"))
        if (
            request.GET.get("uid") != ""
            and request.GET.get("uid") != None
            and request.GET.get("uid") not in uids
        ):
            uids.append(request.GET.get("uid"))
            data["uid"] = uids[uids.__len__() - 1]
    print(uids)

    return render(request, "equipment/set_answer.html", data)


def get_uids(request):
    dicionario = dict(enumerate(uids))
    return JsonResponse(dicionario)


@login_required
def delete_model(request, model_name=None, id=None):
    data = {}
    if model_name:
        if model_name == 'armament':
            Model_armament.objects.get(pk=id).delete()
            data['msm'] = 'Deletado com sucesso!'
                
        elif model_name == 'accessory':
            Model_accessory.objects.get(pk=id).delete()
            data['msm'] = 'Deletado com sucesso!'
                
        elif model_name == 'wearable':
            Model_wearable.objects.get(pk=id).delete()
            data['msm'] = 'Deletado com sucesso!'
                
        elif model_name == 'grenada':
            Model_grenada.objects.get(pk=id).delete()
            data['msm'] = 'Deletado com sucesso!'
            
        else:
            data = {
                'armament': Model_armament.objects.all(),
                'accessory': Model_accessory.objects.all(),
                'wearable': Model_wearable.objects.all(),
                'grenada': Model_grenada.objects.all(),
                'msm': 'Falha no deletar!'
            }
            return render(request, "equipment/models.html", data)
    
        return redirect("manage_model")

    
@login_required
def manage_equipment(request):
    return render(request, "equipment/equipments.html", {'equipments': Equipment.objects.all()})


@login_required
def manage_model(request):
    data = {
        'armament': Model_armament.objects.all(),
        'accessory': Model_accessory.objects.all(),
        'wearable': Model_wearable.objects.all(),
        'grenada': Model_grenada.objects.all(),
    }
    
    return render(request, "equipment/models.html", data)