#from django.shortcuts import render

# Create your views here.
# backend/signing/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SignableDocument
from .serializers import SignableDocumentSerializer

class SignableDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint para carregar e gerir documentos para assinatura.
    """
    serializer_class = SignableDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    # Adicionamos os parsers para suportar o upload de ficheiros
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Garante que cada utilizador só vê os seus próprios documentos
        return SignableDocument.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Associa automaticamente o documento ao utilizador que fez o upload
        serializer.save(owner=self.request.user)
