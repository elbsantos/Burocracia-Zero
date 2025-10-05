# backend/integrations/views.py
import os
import requests
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MoloniConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client_id = os.getenv("MOLONI_CLIENT_ID")
        # Usaremos a variável V2, que aponta para /oauth-callback/
        redirect_uri = os.getenv("MOLONI_REDIRECT_URI_V2")
        
        # O 'state' é uma medida de segurança que associa o pedido ao utilizador
        state = request.user.id 
        
        auth_url = f"https://www.moloni.pt/authorize/?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}"
        
        # Devolvemos o URL para o frontend tratar do redirecionamento
        return Response({'authorization_url': auth_url} )

class MoloniCallbackView(APIView):
    def get(self, request):
        auth_code = request.GET.get('code')
        state = request.GET.get('state')

        if not auth_code or not state:
            return Response({"error": "Parâmetros inválidos no callback."}, status=400)

        # Importamos o modelo aqui para evitar importações circulares
        from users.models import CustomUser
        try:
            user = CustomUser.objects.get(id=state)
        except CustomUser.DoesNotExist:
            return Response({"error": "Utilizador inválido ou 'state' adulterado."}, status=400)

        client_id = os.getenv("MOLONI_CLIENT_ID")
        client_secret = os.getenv("MOLONI_CLIENT_SECRET")
        # Usamos a variável V2 também aqui para consistência
        redirect_uri = os.getenv("MOLONI_REDIRECT_URI_V2")

        token_url = "https://www.moloni.pt/v1/grant/token/"
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri
        }
        
        try:
            response = requests.post(token_url, data=payload )
            response.raise_for_status() # Lança um erro para respostas 4xx/5xx
            token_data = response.json()

            # Guardamos os tokens e a data de expiração no nosso modelo de utilizador
            user.moloni_access_token = token_data['access_token']
            user.moloni_refresh_token = token_data['refresh_token']
            user.moloni_token_expires_at = timezone.now() + timedelta(seconds=token_data['expires_in'])
            user.save()

            # Redireciona para a página de sucesso no frontend
            return redirect("http://localhost:3000/dashboard/integrations?status=success" )

        except requests.exceptions.RequestException as e:
            # Em caso de erro na comunicação com o Moloni, redireciona para uma página de falha
            error_details = str(e)
            if e.response:
                error_details = e.response.json()
            return redirect(f"http://localhost:3000/dashboard/integrations?status=error&details={error_details}" )
