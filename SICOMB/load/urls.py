from django.urls import path
from . import views

urlpatterns = [
    path('fazer_carga/', views.get_policeman, name="fazer_carga" ),
]
