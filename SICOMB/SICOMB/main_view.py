from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from equipment.views import filter_equipment
from police.views import dashboard_police
from django.contrib.auth.models import Group
from django.contrib import messages

def error_page(request):
    return render(request, "error.html")

VIEW_POLICE = dashboard_police
VIEW_ADJUNCT = filter_equipment
VIEW_ADMIN = filter_equipment
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
            messages.error("O usuário não está presente em nenhum grupo de usuário!")
            return VIEW_ERROR(request)
    except Group.DoesNotExist:
        messages.error("O usuário está presente em um grupo de usuário não existente!")
        return VIEW_ERROR(request)