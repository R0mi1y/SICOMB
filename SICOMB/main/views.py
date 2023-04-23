from django.shortcuts import render

# Só serve pra redirecionar pra tela de login por enquanto
def login(request):
    
    return render(request, 'index.html')

