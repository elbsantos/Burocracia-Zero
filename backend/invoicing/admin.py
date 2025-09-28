#from django.contrib import admin

# Register your models here.
# backend/invoicing/admin.py

from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Configuração para mostrar o modelo Client no painel de administração.
    """
    list_display = ('name', 'nif', 'email', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'nif', 'email')
    # Para uma melhor performance, especialmente com muitos utilizadores
    raw_id_fields = ('user',)
