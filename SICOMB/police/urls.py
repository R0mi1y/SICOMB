from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="login"),
    path("register/", views.register_police, name="cadastro"),
    path("search/<str:matricula>/", views.search_police, name="procurar-policial"),
    path("police-page/", views.finalize_cargo, name="finalizar-carga"),
    path("get_login/", views.get_login_police)
]
