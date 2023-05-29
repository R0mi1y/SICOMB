from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="login"),
    path("register/", views.register_police, name="cadastro"),
    path("police-page/", views.finalize_cargo, name="finalizar-carga")
]
