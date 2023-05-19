from django.urls import path
from .views import get_cargo

urlpatterns = [
   path("fazer_carga/", get_cargo, name="fazer_carga"),
]