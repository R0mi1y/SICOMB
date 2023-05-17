from django.shortcuts import render

from police.forms import UserForm
from django.core.cache import cache
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from . import models
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    HttpResponseRedirect("index")


def register(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('')
        
    else:
        form = UserForm()
        return render(request, 'registration/register.html', {'form': form})
