from django.urls import path
from .views import *

# /equipment
urlpatterns = [
    path("cadastro/", register_equipment, name="register_equipment"),
    path("get", get_equipment),
    path("valid_uid", valid_uid),
    path("valid_serial_number/<str:sn>/", valid_serial_number),
    path("set", set_uid),
    path("get_models", get_models_equipment),
]
