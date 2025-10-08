# backend/chatbot/urls.py
from django.urls import path
from .views import whatsapp_webhook

urlpatterns = [
    # Este ficheiro só define o que vem DEPOIS de /api/chatbot/
    path('whatsapp/', whatsapp_webhook, name='whatsapp-webhook'),
]
