from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

# Só serve pra redirecionar pra tela de login por enquanto


def redirect_login(request):
    return redirect('login')
