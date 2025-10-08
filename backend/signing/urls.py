# backend/signing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignableDocumentViewSet

router = DefaultRouter()
router.register(r'documents', SignableDocumentViewSet, basename='signabledocument')

urlpatterns = [
    path('', include(router.urls)),
]
