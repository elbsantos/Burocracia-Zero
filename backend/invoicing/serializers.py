from rest_framework import serializers
from .models import Client, Invoice, InvoiceItem

# --- Serializer de Cliente ---
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'nif', 'address', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# --- Serializers para Faturas ---

class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    Serializer para os itens da fatura.
    """
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'total_price']


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer para a Fatura. Inclui os itens aninhados.
    """
    items = InvoiceItemSerializer(many=True)
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'client', 'client_name', 'document_type', 'status', 
            'issue_date', 'due_date', 'total_amount', 'notes', 
            'external_id', 'items'
        ]
        # O 'client' é write-only, o 'client_name' é read-only
        read_only_fields = ['id', 'issue_date', 'total_amount', 'client_name', 'external_id']
        # Adicionamos 'client' a write_only_fields para que não apareça na representação
        # mas possa ser escrito.
        extra_kwargs = {'client': {'write_only': True}}


    def create(self, validated_data):
        # O 'user' foi adicionado ao validated_data pelo serializer.save(user=...) na view
        items_data = validated_data.pop('items')
        
        # Agora 'user' está em validated_data e será passado para o create
        invoice = Invoice.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
            total_amount += item_data['quantity'] * item_data['unit_price']
        
        invoice.total_amount = total_amount
        invoice.save()
        
        return invoice
