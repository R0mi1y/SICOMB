from django.urls import path
from .views import *

# /equipment
urlpatterns = [
    path("cadastro/", register_equipment, name="register_equipment"), # registra o equipamento
    path("get", get_equipment), # retorna em o equipamento do uid inserido (em formato JSON)
    path("valid_uid", valid_uid), # valida o uid inserido para cadastrar (em formato JSON)
    path("valid_serial_number/<str:sn>/", valid_serial_number), # valida o numero serial pra cadastro (em formato JSON)
    path("set", set_uid), # seta o uid (em formato API)
    # path("get_models", get_models_equipment), # retorna todos os models
]
