import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import serial
from SICOMB.settings import AUX
from equipment.views import filter_equipment
from police.views import dashboard_police
from police.views import dashboard
from django.contrib.auth.models import Group
from django.contrib import messages

def error_page(request):
    return render(request, "error.html")

VIEW_POLICE = dashboard_police
VIEW_ADJUNCT = dashboard
VIEW_ADMIN = dashboard
VIEW_ERROR = error_page


@login_required
def main_view(request):
    if request.user.is_superuser:
        return VIEW_ADMIN(request)
    try:
        police_group = Group.objects.get(name="police")
        adjunct_group = Group.objects.get(name="adjunct")
        
        if police_group in request.user.groups.all():
            return VIEW_POLICE(request)
        elif adjunct_group in request.user.groups.all():
            return VIEW_ADJUNCT(request)
        else:
            print("O usuário não está presente em nenhum grupo de usuário!")
            messages.error(request, "O usuário não está presente em nenhum grupo de usuário!")
            return VIEW_ERROR(request)
    except Group.DoesNotExist:
        print("O usuário está presente em um grupo de usuário não existente!")
        messages.error(request, "O usuário está presente em um grupo de usuário não existente!")
        return VIEW_ERROR(request)


if AUX["SENSOR_RFID"]:
    ser_rfid = None
    while ser_rfid is None:
        try:
            if ser_rfid is not None: ser_rfid.close()
            ser_rfid = serial.Serial(AUX["PORT_RFID"], 115200)
        except Exception as e:
            time.sleep(0.5)
            print(e)
    
    AUX['serial_port_rfid'] = ser_rfid
        
if AUX["SENSOR_FINGERPRINT"]:
    ser_fingerprint = None
    while ser_fingerprint is None:
        try:
            if ser_fingerprint is not None: ser_fingerprint.close()
            ser_fingerprint = serial.Serial(AUX["PORT_FINGERPRINT"], 115200)
        except Exception as e:
            time.sleep(0.5)
            print(e)
        
    AUX['serial_port_fingerprint'] = ser_fingerprint

from .read_sensors import get_uids