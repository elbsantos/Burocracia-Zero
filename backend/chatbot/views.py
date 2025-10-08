# backend/chatbot/views.py
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from users.models import CustomUser
from invoicing.models import Client, Invoice, InvoiceItem
from decimal import Decimal # 1. Importe o tipo Decimal

@csrf_exempt
def whatsapp_webhook(request ):
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').lower().strip()
        from_number = request.POST.get('From', '')
        response_msg = ""

        try:
            user = CustomUser.objects.get(whatsapp_number=from_number)
            
            # --- LÓGICA DE ESTADO ---
            if user.chatbot_state != 'idle':
                
                # ... (estados 'awaiting_nif' e 'awaiting_nif_confirmation' sem alterações) ...
                if user.chatbot_state == 'awaiting_nif':
                    try:
                        client = Client.objects.get(user=user, nif=incoming_msg)
                        response_msg = f"Encontrei: *{client.name}*.\nCorreto? (sim/não)"
                        user.chatbot_state = 'awaiting_nif_confirmation'
                        user.chatbot_context = {'client_id': client.id, 'items': []}
                        user.save()
                    except Client.DoesNotExist:
                        response_msg = "NIF não encontrado. A começar de novo."
                        user.chatbot_state = 'idle'
                        user.chatbot_context = {}
                        user.save()
                
                elif user.chatbot_state == 'awaiting_nif_confirmation':
                    if incoming_msg == 'sim':
                        response_msg = "Ótimo. Envie os itens da fatura, um por um, no formato:\n*<descrição>, <quantidade>, <preço unitário>*\n\nQuando terminar, envie a palavra `fim`."
                        user.chatbot_state = 'awaiting_items'
                        user.save()
                    elif incoming_msg in ['não', 'nao']:
                        response_msg = "Ok, cancelado. A começar de novo."
                        user.chatbot_state = 'idle'
                        user.chatbot_context = {}
                        user.save()
                    else:
                        response_msg = "Por favor, responda apenas com 'sim' ou 'não'."

                # --- ESTADO: AGUARDANDO ITENS ---
                elif user.chatbot_state == 'awaiting_items':
                    if incoming_msg == 'fim':
                        # 2. Lógica para apresentar o resumo
                        context = user.chatbot_context
                        if not context.get('items'):
                            response_msg = "Nenhum item foi adicionado. A cancelar a criação da fatura."
                            user.chatbot_state = 'idle'
                            user.chatbot_context = {}
                            user.save()
                        else:
                            total = sum(Decimal(str(item['quantity'])) * Decimal(str(item['unit_price'])) for item in context['items'])
                            client = Client.objects.get(id=context['client_id'])
                            
                            response_msg = f"Fatura para *{client.name}* pronta.\n"
                            response_msg += f"Total de itens: {len(context['items'])}\n"
                            response_msg += f"Valor Total: *{total:.2f}€*\n\n"
                            response_msg += "Confirma a criação desta fatura? (sim/não)"
                            
                            user.chatbot_state = 'awaiting_final_confirmation'
                            user.save()
                    else:
                        # ... (lógica para adicionar itens, sem alterações) ...
                        parts = [part.strip() for part in incoming_msg.split(',')]
                        if len(parts) != 3:
                            response_msg = "Formato inválido. Preciso de 3 partes: *descrição, quantidade, preço*"
                        else:
                            try:
                                description = parts[0]
                                if not description: raise ValueError("Descrição vazia.")
                                quantity = float(parts[1])
                                unit_price = float(parts[2])
                                context = user.chatbot_context
                                context['items'].append({'description': description, 'quantity': quantity, 'unit_price': unit_price})
                                user.chatbot_context = context
                                user.save()
                                response_msg = f"✅ Item adicionado: *{description}*.\nEnvie o próximo item ou `fim` para terminar."
                            except (ValueError, IndexError):
                                response_msg = "Formato inválido. Quantidade e preço devem ser números."
                
                # --- ESTADO: AGUARDANDO CONFIRMAÇÃO FINAL ---
                elif user.chatbot_state == 'awaiting_final_confirmation':
                    # 3. Lógica para criar a fatura na base de dados
                    if incoming_msg == 'sim':
                        context = user.chatbot_context
                        client = Client.objects.get(id=context['client_id'])
                        
                        # Cria a fatura
                        new_invoice = Invoice.objects.create(
                            user=user,
                            client=client,
                            document_type='FR', # Fatura-Recibo por defeito
                            status='DRAFT'
                        )
                        
                        # Cria os itens da fatura
                        for item_data in context['items']:
                            InvoiceItem.objects.create(
                                invoice=new_invoice,
                                description=item_data['description'],
                                quantity=Decimal(str(item_data['quantity'])),
                                unit_price=Decimal(str(item_data['unit_price']))
                            )
                        
                        response_msg = f"✅ Fatura #{new_invoice.id} criada com sucesso no BurocraciaZero!"
                        
                        user.chatbot_state = 'idle'
                        user.chatbot_context = {}
                        user.save()
                    else: # Se a resposta for 'não' ou qualquer outra coisa
                        response_msg = "Criação da fatura cancelada. A começar de novo."
                        user.chatbot_state = 'idle'
                        user.chatbot_context = {}
                        user.save()

            # Se o estado for 'idle', procuramos por comandos principais
            else:
                # ... (código dos comandos principais 'olá', 'meus clientes', 'nova fatura' - sem alterações) ...
                if incoming_msg in ['olá', 'oi', 'ola']:
                    response_msg = f"Olá {user.get_full_name()}! Comandos disponíveis:\n- meus clientes\n- nova fatura"
                elif incoming_msg == 'meus clientes':
                    clients = Client.objects.filter(user=user).order_by('name')
                    if clients.exists():
                        response_msg = "Aqui estão os seus clientes:\n\n"
                        for client in clients:
                            response_msg += f"👤 *{client.name}*\n   NIF: {client.nif}\n"
                    else:
                        response_msg = "Você ainda não tem nenhum cliente registado."
                elif incoming_msg == 'nova fatura':
                    response_msg = "Ok, vamos criar uma nova fatura. Para qual cliente? Por favor, envie o NIF do cliente."
                    user.chatbot_state = 'awaiting_nif'
                    user.chatbot_context = {}
                    user.save()
                else:
                    response_msg = "Não entendi o seu comando. Comandos disponíveis:\n- meus clientes\n- nova fatura"

        except CustomUser.DoesNotExist:
            response_msg = "O seu número de telefone não está registado no BurocraciaZero."
        
        twiml_response = MessagingResponse()
        twiml_response.message(response_msg)
        return HttpResponse(str(twiml_response), content_type='application/xml')

    return HttpResponse("Endpoint do Webhook. Apenas pedidos POST são aceites.", status=405)
