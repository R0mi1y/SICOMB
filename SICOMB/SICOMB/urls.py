from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .main_view import main_view

urlpatterns = [
    path('', main_view),
    path('admin/', admin.site.urls),
    path('equipamento/', include('equipment.urls')),
    path('carga/', include('load.urls')),
    path('police/', include('police.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
