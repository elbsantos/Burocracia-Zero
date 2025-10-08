# backend/signing/serializers.py
import json # Importe o módulo json
from rest_framework import serializers
from .models import SignableDocument, SignatureRequest

class SignatureRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureRequest
        fields = ['id', 'signer_name', 'signer_email', 'status', 'signed_at']
        read_only_fields = ['id', 'status', 'signed_at']

# NOVO: Um campo de serializer personalizado para lidar com o JSON dentro do FormData
class SignersField(serializers.Field):
    def to_representation(self, value):
        # Isto não será usado, pois o campo é write_only
        return []

    def to_internal_value(self, data):
        # 'data' será a string JSON que o frontend nos envia
        try:
            # Tentamos converter a string de volta para uma lista de objetos Python
            signers_data = json.loads(data)
            if not isinstance(signers_data, list):
                raise serializers.ValidationError("Esperava uma lista de signatários.")
            
            # Validamos cada objeto de signatário individualmente
            signer_serializer = SignatureRequestSerializer(data=signers_data, many=True)
            signer_serializer.is_valid(raise_exception=True)
            return signer_serializer.validated_data

        except json.JSONDecodeError:
            raise serializers.ValidationError("Formato JSON inválido para os signatários.")
        except Exception as e:
            raise serializers.ValidationError(f"Erro na validação dos signatários: {e}")


class SignableDocumentSerializer(serializers.ModelSerializer):
    original_file_url = serializers.CharField(source='original_file.url', read_only=True)
    signature_requests = SignatureRequestSerializer(many=True, read_only=True)
    
    # AQUI ESTÁ A MUDANÇA: Usamos o nosso novo campo personalizado
    signers = SignersField(write_only=True)

    class Meta:
        model = SignableDocument
        fields = [
            'id', 
            'title', 
            'status', 
            'created_at', 
            'original_file',
            'original_file_url',
            'signature_requests',
            'signers'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'original_file_url', 'signature_requests']

    def create(self, validated_data):
        signers_data = validated_data.pop('signers')
        document = SignableDocument.objects.create(**validated_data)
        
        for signer_data in signers_data:
            SignatureRequest.objects.create(document=document, **signer_data)
            
        return document
