from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from equipment.views import manage_equipment

urlpatterns = [
    path('', manage_equipment),
    path('admin/', admin.site.urls),
    path('equipamento/', include('equipment.urls')),
    path('carga/', include('load.urls')),
    path('police/', include('police.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
