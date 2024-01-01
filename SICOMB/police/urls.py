from django.urls import path
from . import views, apis

urlpatterns = [
    path('perfil/<int:id>', views.perfil_police, name="perfil_police"),
    path('filter/', views.filter_police, name="filter_police"),
    path('approve/', views.approve_police, name="approve_police"),
    path("register/", views.register_police, name="register_police"),
    path("login/", views.login, name="login"),
    path("search/<str:id>/", views.search_police, name="procurar-policial"),
    path("reduce/", views.reduce_police, name="reduce_police"),
    path("promote/", views.promote_police, name="promote_police"),
    path("get_login/", apis.get_login_police),
    path("register/fingerprint/<int:police_id>/", apis.fingerprint_register_police, name="register_police"),
    path("get_fingerprint/", apis.get_fingerprint),
    path("request/fingerprint/", apis.request_fingerprint),
    path("fingerprint/delete/<int:police_id>", apis.delete_fingerprint),
]
