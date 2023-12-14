import hashlib
from django.http import JsonResponse
from .models import *
from django.conf import settings
from load.apis import require_user_pass
from django.views.decorators.csrf import csrf_exempt

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
    

@csrf_exempt
@require_user_pass
def get_fingerprint(request):
    # linha = settings.AUX["porta_serial"].readline().decode('utf-8').strip()
    linha = "FINGERPRINT::163516"
    
    print(linha)
            
    linha = linha.split("::")
    if linha[0] == "FINGERPRINT":
        code = linha[1]
        
        police = Police.objects.filter(fingerprint=code).first()
        
        if police is not None:
            settings.AUX["token_login_police"] = calcular_hash(police)
            
            return JsonResponse({"status": True, "matricula": str(police.matricula), "token": settings.AUX["token_login_police"]})
        else:
            return JsonResponse({"status": False, "message": "Policial não vinculado à essa digital"})
    return JsonResponse({"status": False})
        
        
def calcular_hash(police):
    dados = f"{police.matricula}{police.name}{police.fingerprint}"

    hash_obj = hashlib.sha256()
    hash_obj.update(dados.encode('utf-8'))

    hash_result = hash_obj.hexdigest()

    hash_reduzido = hash_result[:5]

    return hash_reduzido