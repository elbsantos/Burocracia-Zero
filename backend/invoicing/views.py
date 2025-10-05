from rest_framework import viewsets, permissions
from .models import Client, Invoice
from .serializers import ClientSerializer, InvoiceSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    Um ViewSet para ver e editar instâncias de clientes.
    """
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todos os clientes
        pertencentes ao utilizador atualmente autenticado.
        """
        return self.request.user.clients.all().order_by('name')

    def perform_create(self, serializer):
        """
        Ao criar um novo cliente, associa-o automaticamente ao
        utilizador que está a fazer o pedido.
        """
        serializer.save(user=self.request.user)


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ver e editar Faturas.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        O utilizador só pode ver as suas próprias faturas.
        """
        return self.request.user.invoices.select_related('client').prefetch_related('items').all().order_by('-issue_date')

    def perform_create(self, serializer):
        """
        Associa a fatura ao utilizador que está a fazer o pedido,
        passando o 'user' para o método 'save' do serializer.
        """
        # Esta linha é a chave da correção.
        # O serializer.save() irá chamar o nosso método create() no serializer,
        # e o 'user' será adicionado ao dicionário 'validated_data'.
        serializer.save(user=self.request.user)
