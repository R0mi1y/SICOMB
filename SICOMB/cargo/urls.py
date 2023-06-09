from django.urls import path
from . import views

urlpatterns = [
    path("fazer_carga/", views.redirect_cargo, name="fazer_carga"),
    path("fazer_carga/confirm", views.confirm_cargo, name="confirmar_carga"),
    path("fazer_carga/cancel", views.cancel_cargo, name="cancelar_carga"),
    path("get/<int:id>/", views.get_cargo, name="get_carga"),
    path("list_equipment/add/<str:serial_number>/<str:obs>/", views.add_list_equipment),
    path(
        "list_equipment/remove/<str:serial_number>/<str:obs>/",
        views.remove_list_equipment,
    ),
    path("list_equipment/get", views.get_list_equipment),
]
