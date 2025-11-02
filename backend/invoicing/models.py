from django.db import models
from decimal import Decimal # Adicionada para garantir o tipo correto no cálculo
from django.conf import settings

# --- Modelo de Cliente ---
class Client(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=20, blank=True, verbose_name="NIF")
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name

# --- Modelo de Fatura ---
class Invoice(models.Model):
    class DocumentType(models.TextChoices):
        FATURA = 'FT', 'Fatura'
        FATURA_RECIBO = 'FR', 'Fatura-Recibo'
        RECIBO = 'RC', 'Recibo'

    class InvoiceStatus(models.TextChoices):
        POR_PAGAR = 'Pendente'
        PAGA = 'Paga'
        ATRASADA = 'Atrasada'
        ANULADA = 'Anulada'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='invoices')
    
    document_type = models.CharField(max_length=2, choices=DocumentType.choices, default=DocumentType.FATURA_RECIBO)
    status = models.CharField(max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.POR_PAGAR)
    
    issue_date = models.DateField(auto_now_add=True, verbose_name="Data de Emissão")
    due_date = models.DateField(null=True, blank=True, verbose_name="Data de Vencimento")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Total")
    notes = models.TextField(blank=True, verbose_name="Notas")

    external_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def calculated_total(self):
        # Calcula o total usando iteração em Python (alternativa para evitar o ImportError)
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price
        return total

    def save(self, *args, **kwargs):
        # Atualiza o total_amount com o valor calculado antes de salvar
        if self.pk:
            self.total_amount = self.calculated_total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_document_type_display()} para {self.client.name} - {self.total_amount}€"

# --- Modelo de Item da Fatura ---
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} ({self.quantity}x{self.unit_price})"