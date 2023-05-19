from django.shortcuts import render
from equipment.views import get_equipment
from django.contrib.auth.decorators import login_required

# Create your views here.
def insert_equipment(request):
    pass

@login_required
def get_cargo(request):
    return render(request, 'equipment/fazer_carga.html')


def finished_cargo(request):
    pass