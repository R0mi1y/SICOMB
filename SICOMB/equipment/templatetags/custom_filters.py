from django import template
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from police.models import Police

register = template.Library()

@register.filter
def model_class(model):
    model_name = {
        'Model_armament': 'Armamento',
        'Model_accessory': 'Acessório',
        'Model_wearable': 'Vestimentos',
        'Model_grenada': 'Granadas',
        'Bullet': 'Munição',
    }
    
    return model_name[model.__class__.__name__]


def require_user_pass(funcao):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            password = request.POST.get('pass')
            user = request.POST.get('user')
            
            if Police.objects.filter(username=user, password=password).exists():
                
                return funcao(request, *args, **kwargs)
            else:
                return JsonResponse({"msm": "Credenciais inválidas"})
        else:
            return JsonResponse({"msm": "Credenciais inválidas"})
        
    return wrapper


def has_group(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Acesso negado. Você não está autenticado.")
            
            # Verifica se o usuário pertence ao grupo especificado
            if request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Acesso negado. Você não tem permissão para acessar esta página.")
        
        return wrapper
    
    return decorator
