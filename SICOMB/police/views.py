from django.shortcuts import render
from police.forms import UserForm
from django.core.cache import cache
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from . import models
from police.forms import PoliceForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    HttpResponseRedirect("index")


def register_police(request):
    
    if request.method == "POST":
        form = PoliceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PoliceForm
           
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