from django.shortcuts import render

# Create your views here.
# backend/invoicing/views.py

from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    Um ViewSet para ver e editar instâncias de clientes.
    Fornece automaticamente as ações `list`, `create`, `retrieve`,
    `update` e `destroy`.
    """
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated] # Apenas utilizadores autenticados podem aceder

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todos os clientes
        pertencentes ao utilizador atualmente autenticado.
        """
        # self.request.user é o utilizador autenticado (graças ao token JWT)
        return self.request.user.clients.all().order_by('name')

    def perform_create(self, serializer):
        """
        Ao criar um novo cliente, associa-o automaticamente ao
        utilizador que está a fazer o pedido.
        """
        serializer.save(user=self.request.user)
