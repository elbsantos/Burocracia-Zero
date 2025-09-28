# backend/invoicing/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet

# Cria um router, que é uma forma do DRF gerar os URLs automaticamente
router = DefaultRouter()
# Regista o nosso ViewSet. O 'r'clients'' é o prefixo do URL (ex: /api/invoicing/clients/)
router.register(r'clients', ClientViewSet, basename='client')

# Os URLs da API são agora determinados automaticamente pelo router.
urlpatterns = [
    path('', include(router.urls)),
]
