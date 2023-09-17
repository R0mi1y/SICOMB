from django.urls import path
from . import views

urlpatterns = [
    path('approve/', views.approve_police, name="approve_police"),
    path("register/", views.register_police, name="cadastro"),
    path("login/", views.login, name="login"),
    path("search/<str:matricula>/", views.search_police, name="procurar-policial"),
    path("reduce/", views.reduce_police, name="rebaixar-adjunto"),
    path("promote/", views.promote_police, name="promover-policial"),
    path("get_login/", views.get_login_police)
]
