from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    operation_id = serializers.UUIDField(
        validators=[UniqueValidator(
            queryset=Payment.objects.all(),
            message="Платеж с таким operation_id уже существует."
        )]
    )

    class Meta:
        model = Payment
        fields = '__all__'
