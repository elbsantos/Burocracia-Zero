from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/invoicing/', include('invoicing.urls')),
    path('api/integrations/', include('integrations.urls')), # Adiciona a nova rota
]
