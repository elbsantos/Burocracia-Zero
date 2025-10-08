# backend/users/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Removemos 'username' e tornamos 'email' o campo de login
    username = None
    email = models.EmailField(unique=True, verbose_name='Endereço de e-mail')
    full_name = models.CharField(max_length=255, verbose_name='Nome Completo')
    whatsapp_number = models.CharField(max_length=30, blank=True, verbose_name='Número do WhatsApp')
    chatbot_state = models.CharField(max_length=50, default='idle', blank=True)
    chatbot_context = models.JSONField(default=dict, blank=True)
    
    # --- Campos de Subscrição ---
    class SubscriptionPlan(models.TextChoices):
        FREE = 'FREE', 'Plano Gratuito'
        BASIC = 'BASIC', 'Plano Básico'
        PREMIUM = 'PREMIUM', 'Plano Premium'

    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Ativa'
        CANCELED = 'CANCELED', 'Cancelada'
        INCOMPLETE = 'INCOMPLETE', 'Incompleta'

    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE
    )
    subscription_status = models.CharField(
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.INCOMPLETE
    )

    # --- NOVOS CAMPOS PARA A INTEGRAÇÃO MOLONI ---
    # Estes campos devem estar aqui, no corpo principal da classe CustomUser
    moloni_access_token = models.CharField(max_length=512, blank=True, null=True)
    moloni_refresh_token = models.CharField(max_length=512, blank=True, null=True)
    moloni_token_expires_at = models.DateTimeField(blank=True, null=True)


    # --- Configuração do Manager ---
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
