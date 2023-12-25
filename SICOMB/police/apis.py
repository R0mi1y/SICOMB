import hashlib
import threading
import time
from django.http import JsonResponse
from .models import *
from django.conf import settings
from load.apis import require_user_pass
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet


@csrf_exempt
@require_user_pass
def get_login_police(request):
    print(settings.AUX["matricula"])
    if settings.AUX["matricula"]:
        try:
            police = Police.objects.get(matricula=settings.AUX["matricula"])
            settings.AUX["matricula"] = ''
            
            police = {
                "foto": police.image_path.url,
                "nome": police.name,
                "matricula": police.matricula,
                "telefone": police.telefone,
                "lotacao": police.lotacao,
                "email": police.email,
            }
        except Police.DoesNotExist:
            return JsonResponse({})
        return JsonResponse(police)
    else:
        return JsonResponse({})
    
    
def calcular_hash(police):
    chave = Fernet.generate_key()
    fernet = Fernet(chave)
    
    dados = f"{police.name}::{police.matricula}::{police.fingerprint}".encode()

    return (chave , fernet.encrypt(dados).decode('latin-1'))


@csrf_exempt
# @require_user_pass
def get_fingerprint(request):
    """
    Função que lê o leitor de impressão digital e retorna encriptografado 
    as informações para que a página submeta

    Returns:
        json: o json terá obrigatóriamento o status, onde será True para 
        impressão encontrada e False para qualquer outra coisa.
        Dentre essas outras coisas ela pode ou simplesmente retornar o false 
        ou retornar um type que conterá o tipo de informação a ser enviado (para popUps e avisos)
    """
    
    if settings.AUX["message_fingerprint_sensor"] is None:
        return JsonResponse({"status": False})
        
    linha = settings.AUX["message_fingerprint_sensor"]
    settings.AUX["message_fingerprint_sensor"] = None
    
    if not linha:
        return JsonResponse({"status": False})
        
    if len(linha) > 0 and linha[1] in "SUCCESS\r\n":
        if settings.AUX['registering_fingerprint']['status']:
            fingerprint = settings.AUX['registering_fingerprint']['fingetprint_id']
            police = settings.AUX['registering_fingerprint']['police_id']
            police = Police.objects.filter(id=police).first()
            
            police.fingerprint = fingerprint
            police.save()
            
            return JsonResponse({"status": False, "type": "SUCCESS", "message": "Digital cadastrada com sucesso!"})
        
        else:
            return JsonResponse({"status": False})
        
    elif len(linha) > 1 and linha[1] in ["USERMESSAGE", "ERROR"]:
        return JsonResponse({"status": False, "type": linha[1], "message": linha[2]})
    
    elif len(linha) > 1:
        police = Police.objects.filter(fingerprint=linha[1]).first()
        
        if police is None:
            return JsonResponse({"status": False, "type": "ERROR", "message": "Policial não encontrado na base de dados!"})
            
        (key, token) = calcular_hash(police)
        settings.AUX["key_token_login_police"] = key # A chave para descriptografar as informações será salva na memória para ser usado depois no login
        return JsonResponse({"status": True, "token": token})
        
    else:
        return JsonResponse({"status": False})


@csrf_exempt
@require_user_pass
def request_fingerprint(request):
    ser = settings.AUX["serial_port_fingerprint"]
    
    ser.write("1".encode())
    return JsonResponse({"status": True})


@csrf_exempt
@require_user_pass
def delete_fingerprint(request, police_id):
    police = Police.objects.filter(id=police_id).first()
    
    if police:
        police.fingerprint = None
        police.save()
    else:
        return JsonResponse({"status": False, "message": "Policial não encontrado!"})
    
    return JsonResponse({"status": True})

    
@csrf_exempt
@require_user_pass
def fingerprint_register_police(request, police_id):
    ser = settings.AUX["serial_port_fingerprint"]
    
    settings.AUX['registering_fingerprint']['status'] = True
    settings.AUX['registering_fingerprint']['police_id'] = police_id
    
    for i in range(1, 1000):
        police = Police.objects.only("fingerprint").filter(fingerprint=i).first()
        if not police:
            ser.write(f"2 {i}".encode())
            settings.AUX['registering_fingerprint']['fingetprint_id'] = i
            break
        
        elif police.fingerprint is not None:
            police.fingerprint = None
            police.save()
            
            return JsonResponse({"message": "O policial já tem uma digital, a digital ira sobrepor a que ele já possui!"})
            
    return JsonResponse({"message": "Cadastrando, caso haja algum erro o policial será alertado"})
