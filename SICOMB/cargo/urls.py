from django.urls import path
from . import views

urlpatterns = [
   path("fazer_carga/", views.get_cargo, name="fazer_carga"),
]