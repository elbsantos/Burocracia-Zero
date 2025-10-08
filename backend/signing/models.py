from django.db import models

# Create your models here.
# backend/signing/models.py
import uuid
from django.db import models
from django.conf import settings

# Função para gerar um caminho de upload único para cada ficheiro
def document_upload_path(instance, filename):
    # O ficheiro será guardado em: media/user_<id>/documents/<uuid>_<filename>
    return f'user_{instance.owner.id}/documents/{uuid.uuid4()}_{filename}'

class SignableDocument(models.Model):
    """
    Representa um documento que foi carregado para ser assinado.
    """
    class DocumentStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        SENT = 'SENT', 'Enviado para Assinatura'
        COMPLETED = 'COMPLETED', 'Concluído'
        VOIDED = 'VOIDED', 'Anulado'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='signable_documents',
        verbose_name="Proprietário"
    )
    title = models.CharField("Título do Documento", max_length=255)
    original_file = models.FileField("Ficheiro Original", upload_to=document_upload_path)
    status = models.CharField(
        "Estado", 
        max_length=10, 
        choices=DocumentStatus.choices, 
        default=DocumentStatus.DRAFT
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f"'{self.title}' de {self.owner.get_full_name()}"

class SignatureRequest(models.Model):
    """
    Representa um pedido de assinatura para um signatário específico.
    """
    class SignatureStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        SIGNED = 'SIGNED', 'Assinado'
        DECLINED = 'DECLINED', 'Recusado'

    document = models.ForeignKey(
        SignableDocument, 
        on_delete=models.CASCADE, 
        related_name='signature_requests',
        verbose_name="Documento"
    )
    signer_name = models.CharField("Nome do Signatário", max_length=255)
    signer_email = models.EmailField("Email do Signatário")
    
    # Um token único para aceder à página de assinatura
    signature_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    status = models.CharField(
        "Estado da Assinatura", 
        max_length=10, 
        choices=SignatureStatus.choices, 
        default=SignatureStatus.PENDING
    )
    
    # Informações que seriam preenchidas pelo serviço de assinatura
    signed_at = models.DateTimeField("Assinado em", null=True, blank=True)
    signed_ip_address = models.GenericIPAddressField("Endereço IP", null=True, blank=True)
    
    # O documento final, assinado, que seria devolvido pelo serviço
    signed_document_file = models.FileField(
        "Ficheiro Assinado", 
        upload_to='signed_documents/', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Pedido de assinatura para {self.signer_email} no documento '{self.document.title}'"
