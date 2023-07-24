from django.urls import path
from .views import *

# /equipment
urlpatterns = [
    path("", manage_equipment, name="manage_equipment"), # mostra a tela de gerencia dos equipamentos
    path("cadastro/", register_edit_equipment, name="register_equipment"), # registra o equipamento
    path("editar/<str:id>", register_edit_equipment, name="edit_equipment"), # registra o equipamento
    path("deletar/<str:id>", delete_equipment, name="delete_equipment"), # registra o equipamento
    
    path("modelos/", manage_model, name="manage_model"), # registra o equipamento
    path("modelo/cadastro/", register_edit_model, name="view_register_model"), # registra o equipamento
    path("modelo/cadastro/<str:model_name>", register_edit_model, name="register_model"), # registra o equipamento
    path("modelo/edit/<str:model_name>/<int:id>", register_edit_model, name="edit_model"), # registra o equipamento
    path("modelo/delete/<str:model_name>/<int:id>", delete_model, name="delete_model"), # registra o equipamento
    
    path("get_disponivel", get_equipment_avalible), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get_indisponivel", get_equipment_unvalible), # retorna em json o equipamento do uid inserido (em formato JSON)
    path("get/<str:serial_number>", get_equipment_serNum), # retorna em o equipamento do uid inserido (em formato JSON)
    path("valid_uid", valid_uid), # valida o uid inserido para cadastrar (em formato JSON)
    path("valid_serial_number/<str:sn>/", valid_serial_number), # valida o numero serial pra cadastro (em formato JSON)
    path("set", set_uid), # seta o uid (em formato API)
    path("lista_espera/get/", get_uids), # seta o uid (em formato API)
    path("bullets/get/", get_bullets), # seta o uid (em formato API)
    # path("get_models", get_models_equipment), # retorna todos os models
]
