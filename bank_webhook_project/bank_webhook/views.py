from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Organization, BalanceLog
from .serializers import PaymentSerializer
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class BankWebhookView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        operation_id = data["operation_id"]

        if Payment.objects.filter(operation_id=operation_id).exists():
            return Response({"detail": "Операция уже обработана"}, status=status.HTTP_200_OK)

        with transaction.atomic():
            Payment.objects.create(**data)
            org, _ = Organization.objects.get_or_create(inn=data["payer_inn"])
            org.balance += data["amount"]
            org.save()

            BalanceLog.objects.create(organization=org, delta=data["amount"])
            logger.info(f"Баланс обновлен: ИНН={org.inn}, Новый баланс={org.balance}")

        return Response({"detail": "Платеж обработан"}, status=status.HTTP_201_CREATED)


class GetBalanceView(APIView):
    def get(self, request, inn):
        try:
            org = Organization.objects.get(inn=inn)
            return Response({"inn": org.inn, "balance": org.balance})
        except Organization.DoesNotExist:
            return Response({"inn": inn, "balance": 0})
