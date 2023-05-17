from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Só serve pra redirecionar pra tela de login por enquanto

@login_required
def redirect_index(request):
    return redirect('register_equipment')
