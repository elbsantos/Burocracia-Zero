# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/invoicing/', include('invoicing.urls')),
    path('api/integrations/', include('integrations.urls')),
    path('api/signing/', include('signing.urls')),    
]

# Adiciona os URLs para servir ficheiros de media em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
