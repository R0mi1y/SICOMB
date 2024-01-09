from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from equipment.templatetags.custom_filters import has_group
from load.models import *
from equipment.models import *
from police.models import *
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .forms import *
from django.contrib import messages


settings.AUX["list_equipment"] = {}  # lista de equipamentos
settings.AUX["list_equipment_removed"] = {}  # lista de equipamentos removidos

# cadastra a carga com a lista
@has_group('adjunct')
def confirm_load(request):
    data = {
        "municoes": settings.AUX["calibres"]
    }
    police = None
    
    if request.method == "POST" and settings.AUX["confirm_cargo"]:
        settings.AUX["matricula"] = ''
        settings.AUX["confirm_cargo"] = False
        
        if len(settings.AUX["list_equipment"]) > 0 or len(settings.AUX["list_equipment_removed"]) > 0:
            turn_type = request.POST.get("turn_type")
            data_hora_atual = datetime.now()  # pega a data atual
            turn_types = ['6H', '12H', '24H', '8H']

            if turn_type in turn_types:
                data_hora_futura = data_hora_atual + timedelta(
                    hours=int(turn_type.replace("H", ""))
                )
            else:
                data_hora_futura = None

            try:
                police = Police.objects.get(matricula=request.POST.get("plate"))
            except Police.DoesNotExist:
                pass

            load = Load(
                expected_load_return_date=data_hora_futura,
                turn_type=turn_type,
                police=police,
                adjunct=request.user,
                status="-",
            )
            load.save()
            
            turn_types += ['REQUISIÇÃO JUDICIAL', 'CONSERTO', 'INDETERMINADO']

            if turn_type in turn_types:
                for key in settings.AUX["list_equipment"]:
                    
                    try:
                        observation = settings.AUX["list_equipment"][key]["observation"]
                    except:
                        observation = "-"
                        
                    
                    if "bullet::" not in key:
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = turn_type
                        equipment.save()

                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=settings.AUX["list_equipment"][key]["amount"],
                        ).save()
                    elif "bullet::" in key:
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ''))
                        amount_to_subtract = int(settings.AUX["list_equipment"][key]["amount"])

                        if bullet.amount - amount_to_subtract < 0:
                            amount_to_subtract = bullet.amount
                            bullet.amount = 0
                            data["msm"] = "Munição insuficiente, munição zerada"
                        else:
                            bullet.amount -= amount_to_subtract

                        bullet.save()
                        
                        equipment_load = Equipment_load.objects.filter(load=load, bullet=bullet).first()
                        
                        if equipment_load is not None:
                            equipment_load.amount = amount_to_subtract
                            equipment_load.save()
                        else:
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=observation,
                                amount=amount_to_subtract,
                            ).save()
                            
                for key in settings.AUX["list_equipment_removed"]:
                    
                    try:
                        observation = settings.AUX["list_equipment_removed"][key]["observation"]
                    except:
                        observation = "-"
                    
                    if "bullet::" not in key:
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = turn_type
                        equipment.save()

                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=settings.AUX["list_equipment_removed"][key]["amount"],
                            status="Pendente",
                        ).save()
                    elif "bullet::" in key:
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ""))

                        Equipment_load(
                            load=load,
                            bullet=bullet,
                            observation=observation,
                            amount=settings.AUX["list_equipment_removed"][key]["amount"],
                            status="Pendente",
                        ).save()
                
                Load.objects.send_relatory(load)

                settings.AUX["matricula"] = ""
                settings.AUX["list_equipment"].clear()
                settings.AUX["list_equipment_removed"].clear()
                
            elif turn_type == "descarga":
                load.returned_load_date = datetime.now()
                load.status = "descarga"
                load.returned_load_date = datetime.now()
                
                load_unload = Load.objects.filter(id=request.POST.get("load_id")).first()
                load.load_unload = load_unload
                load.save()
                
                equipment_load_list = Equipment_load.objects.filter(load=load_unload)
                
                for key in settings.AUX["list_equipment"]:
                    amount = int(settings.AUX["list_equipment"][key]["amount"])
                        
                    try:
                        observation = settings.AUX["list_equipment"][key]["observation"]
                    except:
                        observation = "-"
                    
                    if "bullet::" not in key:
                        load_unload.status = "Descarga da carga " + str(load_unload.pk)
                        load_unload.save()
                        
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = "Disponível"
                        equipment.save()
                        
                        eq_load = equipment_load_list.filter(equipment=equipment).first()
                        eq_load.status = "Devolvido"
                        eq_load.save()
                        
                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=amount,
                            status="Retorno",
                        ).save()
                        
                    elif "bullet::" in key:
                        load_unload.status = "Descarga da carga " + str(load_unload.pk)
                        load_unload.save()
                        
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ''))
                        bullet.amount += amount
                        bullet.save()
                        
                        equipment_load = Equipment_load.objects.filter(load=load_unload, bullet=bullet).first()
                        
                        if equipment_load is not None:
                            if equipment_load.amount - amount > 0:
                                equipment_load.amount -= amount
                                
                                Equipment_load(
                                    load=load_unload,
                                    bullet=bullet,
                                    observation=observation,
                                    amount=amount,
                                    status="Devolvido",
                                ).save()
                                
                                equipment_load.save()
                                
                            elif equipment_load.amount - amount < 0:
                                messages.error(request, "Quantidade incorreta! Munições totalmente devolvidas!")
                                equipment_load.status = "Devolvido"
                                equipment_load.save()
                                
                            else:
                                equipment_load.status = "Devolvido"
                                equipment_load.save()
                            
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=observation,
                                amount=amount,
                                status="Retorno",
                            ).save()
                        else:
                            messages.error(request, "Erro!")
                
                Load.objects.send_relatory(load)
                
                settings.AUX["matricula"] = ""
                
                if load_unload: Load.objects.check_load(load_unload) 
                Load.objects.check_load(load)

                settings.AUX["list_equipment"].clear()
                settings.AUX["list_equipment_removed"].clear()
            else:
                messages.error(request, "Erro, Tipo do turno inválido!")
        elif settings.AUX["list_equipment_valid"]:
            settings.AUX["list_equipment_valid"] = False
            settings.AUX["list_equipment"].clear()
            settings.AUX["list_equipment_removed"].clear()
        elif settings.AUX["list_equipment_valid"]:
            pass
        else:
            messages.error(request, "Lista vazia!")

        data["policial"] = police
    
    for i in Load.objects.all():
        Load.objects.check_load(i)
        
    settings.AUX["matricula"] = ''
    return render(request, "load/load.html", data)


# Cancela a carga e zera as listas
@has_group('adjunct')
def cancel_load(request):
    settings.AUX["list_equipment"].clear()
    settings.AUX["list_equipment_removed"].clear()
    return redirect("fazer_carga")


@has_group('adjunct')
def filter_loads(request):
    queryset = Load.objects.all().exclude(turn_type="descarga")
    
    form = LoadFilterForm(request.GET)
    
    if form.is_valid():
        queryset = form.filter_queryset(queryset)
    
    loads = []
    for i in queryset:
        ec = Equipment_load.objects.filter(load=i)
        loads.append([i, len(ec)])
        
        Load.objects.check_load(i)
    
    context = {
        "loads": loads,
        "filter_form": form
    }
        
    return render(request, "load/filter-load.html", context)


@login_required
def get_carga_policial(request, pk):
    load = get_object_or_404(Load, pk=pk)
    equipment_loads = load.equipment_loads.all()
    return render(request, "load/carga_policial.html", {'load': load, 'equipment_loads': equipment_loads})

