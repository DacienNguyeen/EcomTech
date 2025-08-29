from rest_framework import serializers


class ChargePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash_on_delivery', 'Cash on Delivery')
        ]
    )
    # Mock payment details - in real implementation would be tokenized
    card_number = serializers.CharField(max_length=16, required=False, allow_blank=True)
    card_holder = serializers.CharField(max_length=255, required=False, allow_blank=True)


class PaymentResponseSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField()
    status = serializers.CharField()
    transaction_id = serializers.CharField()
    payment_date = serializers.DateTimeField()
    message = serializers.CharField()


class PaymentStatusSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    status = serializers.CharField()
    transaction_id = serializers.CharField()
    payment_date = serializers.DateTimeField()
    message = serializers.CharField()
