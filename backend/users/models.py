from django.db import models

# Create your models here.
# backend/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Esta classe gere a criação de utilizadores e superutilizadores
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail é obrigatório')
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

# Este é o nosso modelo de utilizador principal
class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    # Planos de Subscrição
    class SubscriptionPlan(models.TextChoices):
        FREE = 'FREE', 'Gratuito'
        ESSENTIAL = 'ESSENTIAL', 'Essencial'
        COMPLETE = 'COMPLETE', 'Completo'

    # Estado da Subscrição
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Ativo'
        CANCELED = 'CANCELED', 'Cancelado'
        TRIAL = 'TRIAL', 'Em Teste'

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    subscription_plan = models.CharField(
        max_length=10,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE
    )
    subscription_status = models.CharField(
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIAL
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define o gestor do modelo
    objects = CustomUserManager()

    # Define o campo de e-mail como o campo de login
    USERNAME_FIELD = 'email'
    # Campos obrigatórios ao criar um superuser pela linha de comando
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
