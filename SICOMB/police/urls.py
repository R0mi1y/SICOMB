from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="login"),
    path("register/", views.register_police, name="cadastro"),
    path("login/", views.login, name="login"),
    path("search/<str:matricula>/", views.search_police, name="procurar-policial"),
    path("promote/<str:id>/", views.promote_police, name="promover-policial"),
    path("promote/", views.promote_police, name="lista-promover-policial"),
    path("police-page/", views.finalize_load, name="finalizar-carga"),
    path("get_login/", views.get_login_police)
]
