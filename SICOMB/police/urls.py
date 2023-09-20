from django.urls import path
from . import views

urlpatterns = [
    path('filter/', views.filter_police, name="filter_police"),
    path('approve/', views.approve_police, name="approve_police"),
    path("register/", views.register_police, name="register_police"),
    path("login/", views.login, name="login"),
    path("search/<str:matricula>/", views.search_police, name="procurar-policial"),
    path("reduce/", views.reduce_police, name="reduce_police"),
    path("promote/", views.promote_police, name="promote_police"),
    path("get_login/", views.get_login_police)
]
