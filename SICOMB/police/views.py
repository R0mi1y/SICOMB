from django.shortcuts import render
from police.forms import UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from police.forms import PoliceForm
from django.contrib.auth.decorators import login_required
from .models import RegisterPolice

# Create your views here.

def index(request):
    HttpResponseRedirect("index")


@login_required
def register_police(request):
    
    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return HttpResponseRedirect('/police/register/')
    else:
        form = PoliceForm()
           
    return render(request, 'police/register_police.html' , context={
        'form': form,
    })


def search_police(request, matricula):
    
    try:
        policial = RegisterPolice.objects.only('matricula').get(matricula=matricula)
    except RegisterPolice.DoesNotExist:
        policial = None
        messages.success(request, 'Policial não encontrado!')
        return HttpResponseRedirect('/police/register/')

    if policial:
        policial.foto = None
    
    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES, instance=policial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atulização realizada com sucesso!')
            return HttpResponseRedirect('/police/register/')
    else:
        form = PoliceForm(instance=policial)
           
    return render(request, 'police/register_police.html' , context={
        'form': form,
    })
    

@login_required
def register_user(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cargo/fazer_carga/')
        else:
            return HttpResponseRedirect('')
        
    else:
        form = UserForm()
        return render(request, 'registration/register.html', {'form': form})
    
    
def finalize_cargo(request):
    return render(request, 'police/police_page.html')