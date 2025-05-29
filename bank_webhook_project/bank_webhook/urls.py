from django.urls import path
from .views import BankWebhookView, GetBalanceView

urlpatterns = [
    path('api/webhook/bank/', BankWebhookView.as_view(), name='bank_webhook'),
    path('api/organizations/<str:inn>/balance/', GetBalanceView.as_view(), name='get_balance'),
]
