from django.urls import path
from .views import register_equipment, get_equipment, set_uid

urlpatterns = [
    path("cadastro/", register_equipment, name="register_equipment"),
    path("get/", get_equipment, name='getEquipment'),
    path("set/", set_uid, name='setEquipment'),
]
