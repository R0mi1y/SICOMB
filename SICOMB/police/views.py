from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from police.forms import PoliceForm
from django.contrib.auth.decorators import login_required
from .models import *
from load.models import Load, Equipment_load
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from load.apis import require_user_pass
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    HttpResponseRedirect("index")


@login_required
def login(request):
    settings.AUX["matricula"] = ''
    data = {"msm": ""}
    if request.method == "POST":
        if not request.POST.get("cancelar"):
            try:
                police = Police.objects.get(
                    matricula=request.POST.get("matricula")
                )
            except Police.DoesNotExist:
                return render(
                    request, "police/request_cargo.html", {"msm": "Matrícula incorreta"}
                )

            if check_password(request.POST.get("senha"), police.password):
                settings.AUX["matricula"] = request.POST.get("matricula")

                data["police"] = police
                loads = Load.objects.filter(police=police)
                data["loads"] = []
                for i in loads:
                    ec = Equipment_load.objects.filter(load=i)
                    data["loads"].append([i, len(ec)])
            else:
                data["msm"] = "Senha incorreta"

    return render(request, "police/request_cargo.html", data)


@login_required
def register_police(request):
    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES)
        if form.is_valid():
            police = form.save()
            
            group, created = Group.objects.get_or_create(name='police')
            police.groups.add(group)
            
            messages.success(request, "Cadastro realizado com sucesso!")
            return HttpResponseRedirect("/police/register/")
        else:
            print("Invalido")
    else:
        form = PoliceForm()

    return render(
        request,
        "police/forms.html",
        # "police/register_police.html",
        context={
            "form": form,
        },
    )


def search_police(request, matricula):
    try:
        policial = Police.objects.only("matricula").get(matricula=matricula)
    except Police.DoesNotExist:
        policial = None
        messages.error(request, "Policial não encontrado!")
        return HttpResponseRedirect("/police/register/")

    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES, instance=policial)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, "Atulização realizada com sucesso!")
            return HttpResponseRedirect("/police/register/")
    else:
        form = PoliceForm(instance=policial)

    return render(
        request,
        "police/forms.html",
        context={
            "form": form,
        },
    )


def dashboard_police(request):
    context = {
        'cargos' : '',
        "loads": [],
    }
    loads = Load.objects.filter(police=request.user)
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        context["loads"].append([i, len(ec)])
    return render(request, "police/police_page.html", context)


@csrf_exempt
@require_user_pass
def get_login_police(request):
    try:
        police = Police.objects.get(matricula=settings.AUX["matricula"])
        # settings.AUX["matricula"] = ""
        caminho_arquivo = police.image_path.url

        police = {
            "foto": caminho_arquivo,
            "nome": police.username,
            "matricula": police.matricula,
            "telefone": police.telefone,
            "lotacao": police.lotacao,
            "email": police.email,
        }
    except Police.DoesNotExist:
        return JsonResponse({})

    return JsonResponse(police)


@login_required
def promote_police(request):
    group, created = Group.objects.get_or_create(name='police')
    
    context = {
        "btn_promote": "REBAIXAR",
        "polices": Police.objects.filter(groups=group),
    }
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            
            police.groups.remove(group)
            group_adjunct, created = Group.objects.get_or_create(name='adjunct')
            police.groups.add(group_adjunct)
            
            context["msm"] = "Promovido com sucesso!"
            return render(request, 'police/promote_police.html', context)
        except:
            context["msm"] = "Falha, já existe um adjunto com esse nome!"
            return render(request, 'police/promote_police.html', context)
        
    return render(request, 'police/promote_police.html', context)


@login_required
def reduce_police(request):
    group, created = Group.objects.get_or_create(name='adjunct')

    context = {
        "btn_promote": "PROMOVER",
        "polices": Police.objects.filter(groups=group)
    }
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            police.groups.add(group)

            group_police, _ = Group.objects.get_or_create(name='police')
            police.groups.remove(group_police)
            
        finally:
            context["msm"] = "Falha, o policial não foi encontrado!"
            return render(request, 'police/reduce_police.html', context)

    return render(request, 'police/promote_police.html', context)