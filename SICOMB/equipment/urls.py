from django.urls import path
from . import views, apis

# /equipment
urlpatterns = [
    path("", views.filter_equipment, name="filter_equipment"), # mostra a tela de gerencia dos equipamentos
    path("approve/", views.approve_equipment, name="approve_equipment"), # mostra a tela de gerencia dos equipamentos
    path("cadastro/", views.register_edit_equipment, name="register_equipment"), # registra o equipamento
    path("editar/<str:id>/", views.register_edit_equipment, name="edit_equipment"), # registra o equipamento
    path("deletar/<str:id>/", views.delete_equipment, name="delete_equipment"), # registra o equipamento
    
    path("modelos/", views.filter_model, name="manage_model"), # registra o equipamento
    path("modelos/approve/", views.approve_model, name="approve_model"), # registra o equipamento
    path("modelo/cadastro/", views.register_edit_model, name="register_model"), # registra o equipamento
    path("modelo/cadastro/<str:model_name>/", views.register_edit_model, name="register_model"), # registra o equipamento
    path("modelo/edit/<str:model_name>/<int:id>/", views.register_edit_model, name="edit_model"), # registra o equipamento
    path("modelo/delete/<str:model_name>/<int:id>/", views.delete_model, name="delete_model"), # registra o equipamento
    
    path("allow_cargo", apis.allow_cargo), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get_disponivel", apis.get_equipment_avalible), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get_indisponivel/<int:id>/", apis.get_equipment_unvalible), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get/<str:serial_number>", apis.get_equipment_serNum), # retorna em o equipamento do uid inserido (em formato JSON)
    path("valid_uid", apis.valid_uid), # valida o uid inserido para cadastrar (em formato JSON)
    path("valid_serial_number/<str:sn>/", apis.valid_serial_number), # valida o numero serial pra cadastro (em formato JSON)
    path("set", apis.set_uid), # seta o uid (em formato API)
    path("lista_espera/get/", apis.get_uids), # seta o uid (em formato API)
    path("bullets/get/", apis.get_bullets), # seta o uid (em formato API)
    # path("get_models", get_models_equipment), # retorna todos os models
    path("<str:pk>/info_equipamento/", views.get_equipment_info, name='get_equipment_info'),
]
