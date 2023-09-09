from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from itertools import chain
from django.db.models import Q


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
    if id:  # Se houver o id, signigica que é uma edição
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

                return redirect("manage_equipment")
            else:
                return render(
                    request, "equipment/register-equipment.html", {"form": form}
                )
    form = EquipmentForm(instance=equipment)  # Se for bem sucedido ele zera o form

    return render(request, "equipment/register-equipment.html", {"form": form})


@login_required
def register_edit_model(request, model_name=None, id=None):
    model = None
    form = None

    if model_name:
        if model_name == "bullet":
            ModelClass = Bullet
            FormClass = BulletForm
        else:
            ModelClass = eval(f"Model_{model_name}")
            FormClass = eval(f"Model_{model_name}Form")

        if id:
            model = get_object_or_404(ModelClass, id=id)

        if request.method == "POST":
            form = FormClass(request.POST, request.FILES, instance=model)

            if form.is_valid():
                form.save()
                return redirect("manage_model")
        else:
            form = FormClass(instance=model)

    return render(
        request, "equipment/form-model.html", {"form": form, "model": model_name}
    )


@login_required
def delete_model(request, model_name=None, id=None):
    data = {}
    if model_name:
        eval(f"Model_{model_name}.objects.get(pk=id).delete()")
        data["msm"] = "Deletado com sucesso!"

        return redirect("manage_model")
    else:
        print("Error delete_model")


@login_required
def manage_model(request):
    data = {
        "armament": Model_armament.objects.all(),
        "accessory": Model_accessory.objects.all(),
        "wearable": Model_wearable.objects.all(),
        "grenada": Model_grenada.objects.all(),
        "bullet": Bullet.objects.all(),
    }

    return render(request, "equipment/models.html", data)


def filter_equipment(request):
    equipment_list = Equipment.objects.all()
    filter_form = EquipmentFilterForm(request.GET)

    if filter_form.is_valid():
        model_name = {
            "model_armament" : 'Armamento',
            "model_accessory" : 'Acessório',
            "model_wearable" : 'Vestimentos',
            "model_grenada" : 'Granadas',
        }
        equipment_list = filter_form.filter_queryset(equipment_list)

    context = {
        'equipment_list': equipment_list,
        'filter_form': filter_form,
        'model_name': model_name,
    }

    return render(request, 'equipment/filter.html', context)


def filter_model(request):
    # Consulta todos os objetos dos diferentes modelos e os concatena
    all_models = list(chain(
        Model_armament.objects.all(),
        Model_accessory.objects.all(),
        Model_wearable.objects.all(),
        Model_grenada.objects.all(),
        Bullet.objects.all()
    ))

    filter_form = ModelFilterForm(request.GET)
    
    if filter_form.is_valid():
        print("valido")
        all_models = filter_form.filter_queryset(all_models)
    
    context = {
        'model_list': all_models,
        'filter_form': filter_form,
        'name': "model_armament"
    }

    return render(request, "equipment/filter_model.html", context)