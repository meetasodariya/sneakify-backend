from rest_framework import serializers
from .models import Payment

class PaymentOrderCreateSerializer(serializers.Serializer):
    order_number = serializers.CharField(required=True)

class PaymentVerifySerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField(required=True)
    razorpay_payment_id = serializers.CharField(required=True)
    razorpay_signature = serializers.CharField(required=True)
    order_number = serializers.CharField(required=True)

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'gateway',
            'gateway_order_id',
            'gateway_payment_id',
            'amount',
            'currency',
            'status',
            'created_at',
        ]
