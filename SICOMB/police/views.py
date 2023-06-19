from django.forms import model_to_dict
from django.shortcuts import render
from police.forms import UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from police.forms import PoliceForm
from django.contrib.auth.decorators import login_required
from .models import *
from load.models import Load, Equipment_load
from django.conf import settings
from django.contrib.auth.hashers import check_password

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
                police = RegisterPolice.objects.get(
                    matricula=request.POST.get("matricula")
                )
            except RegisterPolice.DoesNotExist:
                return render(
                    request, "police/police_page.html", {"msm": "Matrícula incorreta"}
                )

            if check_password(request.POST.get("senha"), police.senha):
                settings.AUX["matricula"] = request.POST.get("matricula")

                data["police"] = police
                loads = Load.objects.filter(police=police)
                data["loads"] = []
                for i in loads:
                    ec = Equipment_load.objects.filter(load=i)
                    data["loads"].append([i, ec.__len__])
            else:
                data["msm"] = "Senha incorreta"

    return render(request, "police/police_page.html", data)


@login_required
def register_police(request):
    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return HttpResponseRedirect("/police/register/")
    else:
        form = PoliceForm()

    return render(
        request,
        "police/register_police.html",
        context={
            "form": form,
        },
    )


def search_police(request, matricula):
    try:
        policial = RegisterPolice.objects.only("matricula").get(matricula=matricula)
    except RegisterPolice.DoesNotExist:
        policial = None
        messages.success(request, "Policial não encontrado!")
        return HttpResponseRedirect("/police/register/")

    if policial:
        policial.foto = None

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
        "police/register_police.html",
        context={
            "form": form,
        },
    )


@login_required
def register_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            print(form)
            print(form)
            print(form)
            return HttpResponseRedirect("/carga/fazer_carga/")
        else:
            return HttpResponseRedirect("")

    else:
        form = UserForm()
        return render(request, "registration/register.html", {"form": form})


def finalize_load(request):
    return render(request, "police/police_page.html")


def get_login_police(request):
    try:
        police = RegisterPolice.objects.get(matricula=settings.AUX["matricula"])
        # settings.AUX["matricula"] = ""
        fieldfile = police.foto
        caminho_arquivo = fieldfile.name

        police = {
            "foto": caminho_arquivo,
            "nome": police.nome,
            "matricula": police.matricula,
            "telefone": police.telefone,
            "lotacao": police.lotacao,
            "email": police.email,
        }
        print(police)
    except RegisterPolice.DoesNotExist:
        print(settings.AUX["matricula"])
        return JsonResponse({})

    return JsonResponse(police)
