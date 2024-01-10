import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import serial
from serial.tools import list_ports
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


def verificar_portas():
    while True:
        for porta in list_ports.comports():
            try:
                ser = serial.Serial(porta.device, baudrate=115200, timeout=2)
                print(f"Tentando porta {porta.device}...")
                
                for i in range(0, 100):
                    time.sleep(1)
                
                    try:
                        resposta = ser.readline().decode('UTF-8')
                        print(resposta)
                        
                        if "FINGERPRINT::SUCCESS::Started" in resposta:
                            print(f"Mensagem 'started' recebida em {porta.device}")
                            ser.write("4".encode())
                            
                            return porta.device

                    except UnicodeDecodeError:
                        print(f"Erro de decodificação em {porta.device}: impossível decodificar como UTF-8")
                            
                ser.write("4".encode())
                ser.close()

            except serial.SerialException:
                print(f"Erro ao abrir a porta {porta.device}")


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
    AUX['PORT_FINGERPRINT'] = verificar_portas()
    
    ser_fingerprint = None
    while ser_fingerprint is None:
        try:
            if ser_fingerprint is not None: ser_fingerprint.close()
            ser_fingerprint = serial.Serial(AUX['PORT_FINGERPRINT'], 115200)
            time.sleep(2)
            ser_fingerprint.write("4".encode())
        except Exception as e:
            time.sleep(0.5)
            print(e)
        
    AUX['serial_port_fingerprint'] = ser_fingerprint

from .read_sensors import get_uids