from django.core.cache import cache
from urllib import response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from . import models

# Create your views here.


def login(request):
    if request.method == 'POST':

        try:
            user = models.Police.objects.get(
                plate=request.POST.get('matricula'), password=request.POST.get('senha'))
        except models.Police.DoesNotExist:
            return render(request, 'main/index.html')

        print(
            f"{user.plate, user.password} {request.POST['matricula']} {request.POST['senha']}")

        if user is not None:
            json = vars(user)
            cache.set("user", user, timeout=(60*60*24))
            return redirect('register_equipment')
        else:
            return render(request, 'main/index.html')

    else:
        return render(request, 'main/index.html')


def register(request):

    if request.method == 'POST':
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/index.html')
      
