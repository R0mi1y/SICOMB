from django.urls import path
from . import views

urlpatterns = [
    path(
        "fazer_carga/", views.confirm_cargo, name="fazer_carga"
    ),  # Redireciona pra página
    path(
        "fazer_carga/confirm", views.confirm_cargo
    ),  # Confirma a carga pela lista na views
    path(
        "fazer_carga/cancel", views.cancel_cargo
    ),  # Cancelar a carga zerando a lista na views
    path(
        "get/<int:id>/", views.get_cargo
    ),  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    path(
        "list_equipment/add/<str:serial_number>/<str:obs>/", views.add_list_equipment
    ),  # adiciona um equipamento à lista na views vindo do front
    path(
        "list_equipment/remove/<str:serial_number>/<str:obs>/",
        views.remove_list_equipment,
    ), # Remove um equipamento da lista na views vindo do front a solicitação
    path("list_equipment/get", views.get_list_equipment),
    # Retorna a lista da views
]
