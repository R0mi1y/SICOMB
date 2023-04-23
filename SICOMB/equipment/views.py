from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

def register_equipment(request):
        context = {}
        if request.method == 'POST':
            # TODO Cadastrar o equipamento
            messages.success(request, "Equipamento cadastrado com sucesso") # TODO vero onde isso será usado
        else:
            return render(request, 'register-equipment.html')

# Retorna o UID mais recente em formato JSON
def get_equipment(request):
    data = {'uid' : settings.AUX['UID']}
    if settings.AUX['UID'] != '':
        settings.AUX['UID'] = ""
    
    return JsonResponse(data)

# Recebe o UID do ESP
def set_uid(request):
    # Armazena o UID recebido numa variável global no arquivo settings
    if request.method == 'POST':
        settings.AUX["UID"] = request.POST.get('uid') # TODO Mudar para método POST aqui e no esp
    elif request.method == 'GET':
        settings.AUX["UID"] = request.GET.get('uid') # TODO Mudar para método POST aqui e no esp
        
    return HttpResponse(f"Sucesso, uid = {settings.AUX['UID']}")