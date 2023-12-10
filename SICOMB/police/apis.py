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