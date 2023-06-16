from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),
    path('cargo/', include('cargo.urls')),
    path('police/', include('police.urls')),
    path('', include('equipment.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
