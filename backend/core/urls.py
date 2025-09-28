# backend/core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/invoicing/', include('invoicing.urls')), # Adicionámos esta linha
]
