# backend/chatbot/views.py
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from users.models import CustomUser

@csrf_exempt
def whatsapp_webhook(request ):
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').lower()
        from_number = request.POST.get('From', '')

        try:
            user = CustomUser.objects.get(whatsapp_number=from_number)
            
            if 'olá' in incoming_msg or 'oi' in incoming_msg:
                response_msg = f"Olá {user.get_full_name()}! Bem-vindo de volta ao BurocraciaZero."
            elif 'clientes' in incoming_msg:
                # Futuramente, aqui chamaremos a lógica para listar os clientes
                response_msg = "Funcionalidade 'Meus Clientes' em desenvolvimento."
            else:
                response_msg = "Não entendi o seu comando. Tente 'olá' ou 'clientes'."

        except CustomUser.DoesNotExist:
            response_msg = "O seu número de telefone não está registado no BurocraciaZero. Por favor, registe-se primeiro."
        
        twiml_response = MessagingResponse()
        twiml_response.message(response_msg)

        return HttpResponse(str(twiml_response), content_type='application/xml')

    return HttpResponse("Endpoint do Webhook. Apenas pedidos POST são aceites.", status=405)
