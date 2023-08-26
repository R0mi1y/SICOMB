from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
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
        print(settings.AUX["list_equipment"])
        print(settings.AUX["list_equipment_removed"])
        if len(settings.AUX["list_equipment"]) > 0 or len(settings.AUX["list_equipment_removed"]) > 0:
            
            turn_type = request.POST.get("turn_type")
            data_hora_atual = datetime.now()  # pega a data atual
            
            if turn_type == "6H" or turn_type == "12H" or turn_type == "24H":
                data_hora_futura = data_hora_atual + timedelta(
                    hours=int(turn_type.replace("H", ""))
                )
            else:
                data_hora_futura = None

            try:
                police = Police.objects.get(matricula=request.POST.get("plate"))
            except:
                pass

            load = Load(
                expected_load_return_date=data_hora_futura,
                turn_type=turn_type,
                police=police,
                adjunct=request.user,
            )  # Cadastra a carga
            load.save()

            if turn_type == "6H" or turn_type == "12H" or turn_type == "24H":
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
                        bullet = Bullet.objects.get(caliber=key)
                        
                        if (int(bullet.amount) - int(settings.AUX["list_equipment"][key]["amount"]) < 0):
                            settings.AUX["list_equipment"][key]["amount"] = bullet.amount
                            bullet.amount = 0
                            data["msm"] = "Munição insuficiente, munição zerada"
                        else:
                            bullet.amount = int(bullet.amount) - int(
                                settings.AUX["list_equipment"][key]["amount"]
                            )
                        bullet.save()
                        
                        equipment_load = Equipment_load.objects.filter(load=load, bullet=bullet).first()
                        
                        if (equipment_load is not None):
                            equipment_load.amount = settings.AUX["list_equipment"][key]["amount"]
                            equipment_load.save()
                        else:
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=settings.AUX["list_equipment"][key]["observation"],
                                amount=settings.AUX["list_equipment"][key]["amount"],
                            ).save()
                            
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
                            status="Pendente",
                        ).save()
                    elif key[0] == ".":  # se for uma munição
                        bullet = Bullet.objects.get(caliber=key)

                        Equipment_load(
                            load=load,
                            bullet=bullet,
                            observation=settings.AUX["list_equipment_removed"][key]["observation"],
                            amount=settings.AUX["list_equipment_removed"][key]["amount"],
                            status="Pendente",
                        ).save()

                settings.AUX["matricula"] = ""

                settings.AUX["list_equipment"].clear()
                settings.AUX["list_equipment_removed"].clear()
                # else:
                #     data["error"] = "Error"
            elif turn_type == "descarga":
                
                load.returned_load_date = datetime.now()
                load.status = "descarga"
                load.save()
                load.returned_load_date = datetime.now()
                
                load_unload = Load.objects.filter(id=request.POST.get("load_id")).first()
                equipment_load_list = Equipment_load.objects.filter(load=load_unload)
                
                # Cadastra a lista de equipamentos na tabela equipment_load
                # com a carga cadastrada e os equipamentos da lista
                for key in settings.AUX["list_equipment"]:
                    if key.isdigit() or "ac" in key:
                        load_unload.status = "Parcialmente devolvido"
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = "Disponível"
                        equipment.save()
                        
                        eq_load = equipment_load_list.filter(equipment=equipment).first()
                        eq_load.status = "Devolvido"
                        eq_load.save()
                        
                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=settings.AUX["list_equipment"][key]["observation"],
                            amount=settings.AUX["list_equipment"][key]["amount"],
                        ).save()
                        
                    elif key[0] == ".":  # se for uma munição
                        load_unload.status = "Parcialmente devolvido"
                        bullet = Bullet.objects.get(caliber=key)
                        bullet.amount += int(settings.AUX["list_equipment"][key]["amount"])
                        bullet.save()
                        
                        equipment_load = Equipment_load.objects.filter(load=load, bullet=bullet).first()
                        
                        if (equipment_load is not None):
                            equipment_load.amount = settings.AUX["list_equipment"][key]["amount"]
                            equipment_load.save()
                        else:
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=settings.AUX["list_equipment"][key]["observation"],
                                amount=settings.AUX["list_equipment"][key]["amount"],
                            ).save()
                            
                for key in settings.AUX["list_equipment_removed"]:
                    if key.isdigit() or "ac" in key:
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = "Disponível"
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
            else:
                data["error"] = "Error"

        data["policial"] = police

    return render(request, "load/load.html", data)


# Cancela a carga e zera as listas
def cancel_load(request):
    settings.AUX["list_equipment"].clear()
    settings.AUX["list_equipment_removed"].clear()

    return redirect("fazer_carga")


def get_dashboard_loads(request):
    loads = Load.objects.all().exclude(turn_type="descarga")
    loads_aux = []
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        loads_aux.append([i, ec.__len__])
        
        check_load(i)
        
    return render(request, "load/dashboard-load.html", {"loads": loads_aux})

def get_carga_policial(request, pk):
    load = get_object_or_404(Load, pk=pk)
    equipment_loads = load.equipment_load_set.all()
    return render(request, "load/carga_policial.html", {'load': load, 'equipment_loads': equipment_loads})


def check_load(load):
    data_hora_atual = timezone.now()
    expected_return_date = load.expected_load_return_date
    
    # se tem alguma que já foi devolvida
    has_devolved = load.equipment_loads.filter(status='Devolvido').exists()
    # se tem alguma que ainda não foi devolvida
    has_not_devolved = load.equipment_loads.exclude(status='Devolvido').exists()
    
    if expected_return_date:
        if data_hora_atual > expected_return_date:
            if has_devolved:
                if has_not_devolved:
                    load.status = 'PARCIALMENTE DESCARREGADA COM ATRASO'
                else:
                    load.status = 'DESCARREGADA COM ATRASO'
            else:
                load.status = 'ATRASADA'
        else:
            if has_devolved:
                if has_not_devolved:
                    load.status = 'PARCIALMENTE DESCARREGADA'
                else:
                    load.status = 'DESCARREGADA'
            else:
                load.status = 'DENTRO DO PRAZO'
    else:
        load.status = 'DATA DE RETORNO NÃO DEFINIDA'
        
    load.save()
    return True

        