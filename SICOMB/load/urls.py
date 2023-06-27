from django.urls import path
from . import views

urlpatterns = [
    path(
        "fazer_carga/", views.confirm_load, name="fazer_carga"
    ),  # Redireciona pra página
    path(
        "fazer_carga/cancelar", views.cancel_load
    ),  # Cancelar a carga zerando a lista na views
    path(
        "get/<int:id>/", views.get_load
    ),  # Retorna uma resposta JSON com todas as cargas (caso necessário)
    path(
        "get/cargas_policial/<str:plate>/", views.get_loads_police
    ),  # Retorna uma resposta JSON com todas as cargas do policial com filtro por matricula (caso necessário)
    path(
        "lista_equipamentos/add/<str:serial_number>/<str:obs>/<str:amount>/",
        views.add_list_equipment,
    ),  # adiciona um equipamento à lista na views vindo do front
    path(
        "lista_equipamentos/remover/<str:serial_number>/<str:obs>/<str:amount>/",
        views.remove_list_equipment,
    ),  # Remove um equipamento da lista na views vindo do front a solicitação
    path("lista_equipamentos/get", views.get_list_equipment),
    # Retorna a lista da views
    path("dashboard_cargas/", views.get_dashboard_loads, name='dashboard_cargas'),
    #Retorna a o policial resposável pela carga e a lista de equipamentos da carga
    path("<str:pk>/carga_policial/", views.get_carga_policial, name='carga_polical'),
]
