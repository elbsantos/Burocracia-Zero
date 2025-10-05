from django.urls import path
from .views import MoloniConnectView, MoloniCallbackView

urlpatterns = [
    path('moloni/connect/', MoloniConnectView.as_view(), name='moloni-connect'),
    path('moloni/oauth-callback/', MoloniCallbackView.as_view(), name='moloni-callback'),
]
