# backend/invoicing/serializers.py

from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Client.
    """
    class Meta:
        model = Client
        # Campos a serem incluídos na API. 'user' não é incluído porque
        # será associado automaticamente com base no utilizador autenticado.
        fields = ['id', 'name', 'nif', 'address', 'email', 'created_at', 'updated_at']
        
        # Campos que não podem ser escritos diretamente através da API
        read_only_fields = ['id', 'created_at', 'updated_at']
