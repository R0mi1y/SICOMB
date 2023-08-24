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
            )  # Cadastra a carga
            load.save()

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
        else:
            data["error"] = "Error"
            print("==< error >==")
            print("Não há equipamentos na lista de equipamentos!")

        data["policial"] = police

    return render(request, "load/load.html", data)


# Cancela a carga e zera as listas
def cancel_load(request):
    settings.AUX["list_equipment"].clear()
    settings.AUX["list_equipment_removed"].clear()

    return redirect("fazer_carga")


def get_dashboard_loads(request):
    loads = Load.objects.all()
    loads_aux = []
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        loads_aux.append([i, ec.__len__])
        
        data_hora_atual = timezone.now()
        expected_return_date = i.expected_load_return_date
        if expected_return_date is not None:
            if data_hora_atual > expected_return_date:
                i.status = 'ATRASADA'
            elif data_hora_atual < expected_return_date:
                i.status = 'DENTRO DO PRAZO'
            elif i.returned_load_date > expected_return_date:
                i.status = 'DESCARREGADA COM ATRASO'
            elif i.returned_load_date < expected_return_date:
                i.status = 'DESGARREGADA DENTRO DO PRAZO'
        else:
            i.status = 'DATA DE RETORNO NÃO DEFINIDA'
        
    return render(request, "load/dashboard-load.html", {"loads": loads_aux})

def get_carga_policial(request, pk):
    print("Chegou em carga_policial")
    load = get_object_or_404(Load, pk=pk)
    equipment_loads = load.equipment_load_set.all()
    print(load)
    print(equipment_loads)
    return render(request, "load/carga_policial.html", {'load': load, 'equipment_loads': equipment_loads})
    
    
