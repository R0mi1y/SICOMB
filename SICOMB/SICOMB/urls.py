from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('equipment/', include('equipment.urls')),
    path('police/', include('police.urls')),
    path('cargo/', include('cargo.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
]