from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone
import uuid
import random

from apps.orders.models import Order
from apps.payments.models import Payment
from .serializers import ChargePaymentSerializer, PaymentResponseSerializer, PaymentStatusSerializer


def require_customer_session(request):
    """Check if customer is logged in"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    return customer_id


def mock_payment_processing(payment_method, amount):
    """Mock payment gateway processing"""
    # Simulate different payment outcomes
    success_rate = {
        'credit_card': 0.95,
        'debit_card': 0.93,
        'paypal': 0.98,
        'bank_transfer': 0.99,
        'cash_on_delivery': 1.0  # Always succeeds
    }
    
    rate = success_rate.get(payment_method, 0.9)
    is_success = random.random() < rate
    
    if is_success:
        return {
            'status': 'completed',
            'transaction_id': f'TXN_{uuid.uuid4().hex[:12].upper()}',
            'message': 'Payment processed successfully'
        }
    else:
        return {
            'status': 'failed',
            'transaction_id': None,
            'message': 'Payment declined by bank'
        }


@extend_schema(
    tags=["payments"],
    request=ChargePaymentSerializer,
    responses={200: PaymentResponseSerializer}
)
@api_view(['POST'])
def charge_payment(request):
    """Process payment for an order (mock implementation)"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = ChargePaymentSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        order_id = data['order_id']
        payment_method = data['payment_method']
        
        # Verify order exists and belongs to customer
        try:
            order = Order.objects.get(OrderID=order_id, CustomerID=customer_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if order is payable
        if order.Status not in ['pending', 'confirmed']:
            return Response(
                {"error": f"Cannot process payment for order with status: {order.Status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if payment already exists
        existing_payment = Payment.objects.filter(
            OrderID=order_id, 
            Status__in=['completed', 'processing']
        ).first()
        if existing_payment:
            return Response(
                {"error": "Payment already processed for this order"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mock payment processing
        payment_result = mock_payment_processing(payment_method, order.TotalAmount)
        
        # Create payment record
        payment = Payment(
            OrderID=order_id,
            Amount=order.TotalAmount,
            PaymentMethod=payment_method,
            Status=payment_result['status'],
            TransactionID=payment_result['transaction_id'],
            PaymentDate=timezone.now()
        )
        payment.save()
        
        # Update order status based on payment result
        if payment_result['status'] == 'completed':
            order.Status = 'confirmed'
            order.save()
        
        # Return payment response
        payment_data = {
            'payment_id': payment.PaymentID,
            'order_id': order_id,
            'amount': payment.Amount,
            'payment_method': payment.PaymentMethod,
            'status': payment.Status,
            'transaction_id': payment.TransactionID or '',
            'payment_date': payment.PaymentDate,
            'message': payment_result['message']
        }
        
        response_serializer = PaymentResponseSerializer(payment_data)
        return Response(response_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["payments"],
    responses={200: PaymentStatusSerializer}
)
@api_view(['GET'])
def get_payment_status(request, payment_id):
    """Get payment status"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        payment = Payment.objects.get(PaymentID=payment_id)
        # Verify payment belongs to customer's order
        order = Order.objects.get(OrderID=payment.OrderID, CustomerID=customer_id)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return Response(
            {"error": "Payment not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    status_messages = {
        'pending': 'Payment is being processed',
        'processing': 'Payment is in progress',
        'completed': 'Payment completed successfully',
        'failed': 'Payment failed',
        'refunded': 'Payment has been refunded'
    }
    
    payment_data = {
        'payment_id': payment.PaymentID,
        'status': payment.Status,
        'transaction_id': payment.TransactionID or '',
        'payment_date': payment.PaymentDate,
        'message': status_messages.get(payment.Status, 'Unknown status')
    }
    
    serializer = PaymentStatusSerializer(payment_data)
    return Response(serializer.data)


@extend_schema(
    tags=["payments"],
    responses={200: PaymentStatusSerializer}
)
@api_view(['GET'])
def get_order_payment(request, order_id):
    """Get payment info for an order"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        order = Order.objects.get(OrderID=order_id, CustomerID=customer_id)
        payment = Payment.objects.filter(OrderID=order_id).first()
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not payment:
        return Response(
            {"error": "No payment found for this order"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    status_messages = {
        'pending': 'Payment is being processed',
        'processing': 'Payment is in progress',
        'completed': 'Payment completed successfully',
        'failed': 'Payment failed',
        'refunded': 'Payment has been refunded'
    }
    
    payment_data = {
        'payment_id': payment.PaymentID,
        'status': payment.Status,
        'transaction_id': payment.TransactionID or '',
        'payment_date': payment.PaymentDate,
        'message': status_messages.get(payment.Status, 'Unknown status')
    }
    
    serializer = PaymentStatusSerializer(payment_data)
    return Response(serializer.data)
