from django.urls import path
from .views import register_equipment, get_equipment, set_uid, get_models_equipment

# /equipment
urlpatterns = [
    path("cadastro/", register_equipment, name="register_equipment"),
    path("get", get_equipment),
    path("set", set_uid),
    path("get_models", get_models_equipment),
]
