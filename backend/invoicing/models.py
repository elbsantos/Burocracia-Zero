#from django.db import models
# Create your models here.
# backend/invoicing/models.py
from django.db import models
from django.conf import settings # Para ligar ao nosso CustomUser

class Client(models.Model):
    # Liga cada cliente ao utilizador que o criou
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=20, blank=True, verbose_name="NIF") # Número de Identificação Fiscal
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Garante que um utilizador não pode ter dois clientes com o mesmo nome
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name
