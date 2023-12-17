from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from equipment.models import Equipment
from equipment.templatetags.custom_filters import has_group
from police.forms import PoliceFilterForm, PoliceForm
from django.contrib.auth.decorators import login_required
from .models import *
from load.models import Load, Equipment_load
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from load.apis import require_user_pass
from django.views.decorators.csrf import csrf_exempt


@login_required
def login(request):
    settings.AUX["matricula"] = ''
    data = {}
    if request.method == "POST":
        if not request.POST.get("cancelar"):
            try:
                police = Police.objects.get(
                    matricula=request.POST.get("matricula")
                )
                
            except Police.DoesNotExist:
                messages.error(request, "Matrícula incorreta!")
                
                return render(
                    request, "police/request_cargo.html"
                )
            
            if request.POST.get("type_login") == "password":
                if check_password(request.POST.get("senha"), police.password):
                    if not police.activated:
                        messages.error(request, "Policial aguardando aprovação de um administrador!")
                        
                        return render(request, "police/request_cargo.html", data)
                    
                    settings.AUX["confirmCargo"] = False
                    
                    settings.AUX["matricula"] = request.POST.get("matricula")

                    data["police"] = police
                    loads = Load.objects.filter(police=police).order_by('-date_load')[:15]
                    data["loads"] = []
                    for i in loads:
                        ec = Equipment_load.objects.filter(load=i)
                        data["loads"].append([i, len(ec)])
                else:
                    messages.error(request, "Senha incorreta!")
                    
            if request.POST.get("type_login") == "fingerprint":
                if request.POST.get("token") != settings.AUX["token_login_police"]:
                    print(request.POST.get("token")) 
                    print(settings.AUX["token_login_police"])
                    messages.error(request, "Token de acesso incoerente!")
                else:
                    if not police.activated:
                        messages.error(request, "Policial aguardando aprovação de um administrador!")
                        
                        return render(request, "police/request_cargo.html", data)
                    
                    settings.AUX["confirmCargo"] = False
                    
                    settings.AUX["matricula"] = request.POST.get("matricula")

                    data["police"] = police
                    loads = Load.objects.filter(police=police).order_by('-date_load')[:15]
                    data["loads"] = []
                    
                    for i in loads:
                        ec = Equipment_load.objects.filter(load=i)
                        data["loads"].append([i, len(ec)])
            settings.AUX["token_login_police"] = None


    return render(request, "police/request_cargo.html", data)


@has_group('adjunct')
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
        context={
            "form": form,
        },
    )


@has_group('adjunct')
def search_police(request, id):
    try:
        policial = Police.objects.only("id").get(id=id)
    except Police.DoesNotExist:
        policial = None
        messages.error(request, "Policial não encontrado!")
        return HttpResponseRedirect("/police/register/")

    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES, instance=policial)
        
        if form.is_valid():
            
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


@login_required
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


@has_group('admin')
def promote_police(request):
    group, created = Group.objects.get_or_create(name='police')
    police_list = Police.objects.filter(groups=group, activated=True)
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "PROMOVER",
        "police_list": police_list,
        'filter_form': filter_form,
    }
    
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            
            police.groups.remove(group)
            group_adjunct, created = Group.objects.get_or_create(name='adjunct')
            police.groups.add(group_adjunct)
            
            context["msm"] = "Promovido com sucesso!"
            return render(request, 'police/manage_police.html', context)
        except:
            context["msm"] = "Falha, já existe um adjunto com esse nome!"
            return render(request, 'police/manage_police.html', context)
        
    return render(request, 'police/manage_police.html', context)


@has_group('admin')
def reduce_police(request):
    group, created = Group.objects.get_or_create(name='adjunct')
    police_list = Police.objects.filter(groups=group, activated=True)
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "REBAIXAR",
        "police_list": police_list,
        'filter_form': filter_form,
    }

    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            police.groups.add(group)

            group_police, _ = Group.objects.get_or_create(name='police')
            police.groups.remove(group_police)
            
        except Police.DoesNotExist:
            context["msm"] = "Falha, o policial não foi encontrado!"
            return render(request, 'police/reduce_police.html', context)

    return render(request, 'police/manage_police.html', context)


@has_group('admin')
def approve_police(request):
    police_list = Police.objects.filter(activated=False)
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "APROVAR",
        "police_list": police_list,
        'filter_form': filter_form,
    }
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            
            police.activated = True
            police.activator = request.user
            
            police.save()
            
        except Police.DoesNotExist:
            messages.error(request, "Falha, o policial não foi encontrado!")
            
            return render(request, 'police/reduce_police.html', context)

    return render(request, 'police/manage_police.html', context)


@has_group('adjunct')
def filter_police(request):
    police_list = Police.objects.all()
    filter_form = PoliceFilterForm(request.GET)
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            request.method = "GET"
            
            return HttpResponseRedirect("/police/search/" + id + "/")
        except Police.DoesNotExist:
            messages.error(request, "Falha, o policial não foi encontrado!")
            
            return render(request, 'police/reduce_police.html', context)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "EDITAR",
        'police_list': police_list,
        'filter_form': filter_form,
    }

    return render(request, 'police/manage_police.html', context)

# def filter_police(request):
    # context = {
        
    #     "polices": Police.objects.filter(activated=True)
    # }
    



def dashboard(request):
    data = {
        "loads": {
            "total": Load.objects.all().exclude(status="descarga").count(),
            "completed": Load.objects.filter(status="DESCARREGADA").count(),
            "pending": Load.objects.all().exclude(status="descarga").exclude(status="DESCARREGADA").count(),
        },
        "equipment": {
            "total": Equipment.objects.all().count(),
            "available": Equipment.objects.filter(status="disponível").count(),
            "unavailable": Equipment.objects.all().exclude(status="disponível").count(),
            "repair": Equipment.objects.all().filter(status="CONSERTO").count(),
            "judicial_request": Equipment.objects.all().filter(status="REQUISIÇÃO JUDICIAL").count(),
        },
        "police": {
            "total": Police.objects.all().count(),
            "inactive": Police.objects.filter(activated=False).count(),
        },
    }
    
    return render(request, 'dashboard.html', data)