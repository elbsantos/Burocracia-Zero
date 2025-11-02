from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal, InvalidOperation
import json

from users.models import CustomUser
from invoicing.models import Client, Invoice, InvoiceItem

# --- Funções Auxiliares ---

def send_whatsapp_message(to_number, message_body ):
    # Esta função deve ser implementada para enviar mensagens via Twilio
    # Por enquanto, apenas simula o envio
    print(f"Enviando para {to_number}: {message_body}")
    pass

def get_user_from_whatsapp(whatsapp_number):
    # O número do WhatsApp vem no formato 'whatsapp:+55...'
    # Precisamos normalizar para buscar no banco
    normalized_number = whatsapp_number.split(':')[-1]
    try:
        user = CustomUser.objects.get(whatsapp_number=normalized_number)
        return user
    except CustomUser.DoesNotExist:
        # Se o usuário não existe, ele será criado no fluxo de onboarding
        return None

def handle_onboarding(user, from_number, message_body):
    # Simplesmente cria o usuário se não existir
    if not user:
        user = CustomUser.objects.create(
            username=from_number.split(':')[-1],
            whatsapp_number=from_number.split(':')[-1],
            chatbot_state='idle'
        )
        resp = MessagingResponse()
        resp.message("Olá! Bem-vindo ao BurocraciaZero. Para começar, digite 'olá'.")
        return resp
    return None

# --- Lógica do Chatbot ---

class ChatbotView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_msg = request.POST.get('Body', '').lower().strip()
        from_number = request.POST.get('From', '')
        
        user = get_user_from_whatsapp(from_number)
        
        # 1. Onboarding
        onboarding_response = handle_onboarding(user, from_number, incoming_msg)
        if onboarding_response:
            return HttpResponse(str(onboarding_response), content_type='application/xml')

        # 2. Resposta TwiML
        resp = MessagingResponse()
        
        # 3. Tratamento de Comandos
        if incoming_msg == 'olá':
            user.chatbot_state = 'idle'
            user.chatbot_context = {}
            user.save()
            resp.message("Olá! Eu sou o BurocraciaZero. O que você gostaria de fazer?\n\n* Digite 'nova fatura' para emitir um documento.\n* Digite 'meus clientes' para gerenciar seus clientes.")
        
        elif incoming_msg == 'nova fatura':
            user.chatbot_state = 'awaiting_nif'
            user.chatbot_context = {'items': []}
            user.save()
            resp.message("Para quem é a fatura? Por favor, digite o NIF do cliente.")
        
        # 4. Tratamento de Estados
        elif user.chatbot_state == 'awaiting_nif':
            nif = incoming_msg
            try:
                client = Client.objects.get(user=user, nif=nif)
                user.chatbot_context['client_id'] = client.id
                user.chatbot_state = 'awaiting_items'
                user.save()
                resp.message(f"Cliente {client.name} encontrado. Agora, adicione os itens da fatura no formato: *descrição, quantidade, preço unitário*.\n\nExemplo: Consultoria, 1, 780.80\n\nQuando terminar, digite 'finalizar'.")
            except Client.DoesNotExist:
                # Fluxo de criação de novo cliente simplificado
                user.chatbot_context['temp_nif'] = nif
                user.chatbot_state = 'awaiting_client_name'
                user.save()
                resp.message(f"Cliente com NIF {nif} não encontrado. Por favor, digite o nome completo do cliente.")

        elif user.chatbot_state == 'awaiting_client_name':
            client_name = incoming_msg
            nif = user.chatbot_context.get('temp_nif')
            
            with transaction.atomic():
                client = Client.objects.create(user=user, name=client_name, nif=nif)
                user.chatbot_context['client_id'] = client.id
                user.chatbot_state = 'awaiting_items'
                user.save()
            
            resp.message(f"Cliente {client_name} criado com sucesso. Agora, adicione os itens da fatura no formato: *descrição, quantidade, preço unitário*.\n\nExemplo: Consultoria, 1, 780.80\n\nQuando terminar, digite 'finalizar'.")

        elif user.chatbot_state == 'awaiting_items':
            if incoming_msg == 'finalizar':
                if not user.chatbot_context.get('items'):
                    resp.message("A fatura não possui itens. Por favor, adicione pelo menos um item ou digite 'cancelar'.")
                else:
                    # 5. Finalização da Fatura
                    client_id = user.chatbot_context.get('client_id')
                    client = get_object_or_404(Client, id=client_id)
                    
                    # Cria a Fatura
                    invoice = Invoice.objects.create(
                        user=user,
                        client=client,
                        document_type=Invoice.DocumentType.FATURA_RECIBO,
                        status=Invoice.InvoiceStatus.POR_PAGAR
                    )
                    
                    # Cria os Itens da Fatura
                    for item_data in user.chatbot_context['items']:
                        try:
                            quantity = Decimal(item_data['quantity'])
                            unit_price = Decimal(item_data['unit_price'])
                            
                            InvoiceItem.objects.create(
                                invoice=invoice,
                                description=item_data['description'],
                                quantity=quantity,
                                unit_price=unit_price
                            )
                            
                        except InvalidOperation:
                            # Isso não deve acontecer se a validação for feita antes, mas é uma segurança
                            print(f"Erro de operação inválida ao processar item: {item_data}")
                            continue
                    
                    # CORREÇÃO: Chamamos save() para que o método save() sobrescrito no modelo Invoice
                    # calcule e salve o total_amount correto.
                    invoice.save()
                    
                    # Atualiza o estado do usuário
                    user.chatbot_state = 'idle'
                    user.chatbot_context = {}
                    user.save()
                    
                    # Monta a mensagem de resumo
                    resumo = f"Fatura-Recibo criada com sucesso para {client.name}!\n\n"
                    resumo += "Itens:\n"
                    for item_data in user.chatbot_context['items']:
                        resumo += f"- {item_data['description']} ({item_data['quantity']}x{item_data['unit_price']}€)\n"
                    
                    # Agora que invoice.save() foi chamado, o total_amount está correto.
                    resumo += f"\n*Valor Total: {invoice.total_amount}€*"
                    
                    resp.message(resumo)
                    
            elif incoming_msg == 'cancelar':
                user.chatbot_state = 'idle'
                user.chatbot_context = {}
                user.save()
                resp.message("Criação de fatura cancelada. Digite 'olá' para recomeçar.")
            
            else:
                # Adiciona um novo item
                try:
                    parts = [p.strip() for p in incoming_msg.split(',')]
                    if len(parts) != 3:
                        raise ValueError("Formato incorreto.")
                    
                    description = parts[0]
                    quantity = Decimal(parts[1])
                    unit_price = Decimal(parts[2])
                    
                    if quantity <= 0 or unit_price <= 0:
                        raise ValueError("Quantidade e preço unitário devem ser positivos.")
                    
                    item_data = {
                        'description': description,
                        'quantity': str(quantity),
                        'unit_price': str(unit_price)
                    }
                    user.chatbot_context['items'].append(item_data)
                    user.save()
                    
                    resp.message(f"Item adicionado: {description} ({quantity}x{unit_price}€). Digite o próximo item ou 'finalizar'.")
                    
                except (ValueError, InvalidOperation):
                    resp.message("Formato inválido. Por favor, use: *descrição, quantidade, preço unitário*.\n\nExemplo: Consultoria, 1, 780.80")

        else:
            resp.message("Comando não reconhecido. Digite 'olá' para ver as opções.")

        return HttpResponse(str(resp), content_type='application/xml')
