from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, InvoiceViewSet

# Cria um router, que é uma forma do DRF gerar os URLs automaticamente
router = DefaultRouter()
# Regista o ViewSet de Clientes
router.register(r'clients', ClientViewSet, basename='client')
# Regista o ViewSet de Faturas
router.register(r'invoices', InvoiceViewSet, basename='invoice')

# Os URLs da API são agora determinados automaticamente pelo router.
urlpatterns = [
    path('', include(router.urls)),
]
