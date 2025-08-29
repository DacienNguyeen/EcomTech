from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from decimal import Decimal

from apps.orders.models import Order, OrderDetail
from apps.catalog.models import Book
from .serializers import (
    CreateOrderSerializer,
    OrderResponseSerializer,
    OrderListSerializer,
    UpdateOrderStatusSerializer
)


def require_customer_session(request):
    """Check if customer is logged in"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    return customer_id


@extend_schema(
    tags=["orders"],
    request=CreateOrderSerializer,
    responses={201: OrderResponseSerializer}
)
@api_view(['POST'])
def create_order(request):
    """Create order from cart or explicit items"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        if data.get('from_cart', True):
            # Create order from cart
            cart_items = request.session.get('cart', {})
            if not cart_items:
                return Response(
                    {"error": "Cart is empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            items_data = []
            for book_id_str, quantity in cart_items.items():
                book_id = int(book_id_str)
                try:
                    book = Book.objects.get(BookID=book_id)
                    items_data.append({
                        'book_id': book_id,
                        'quantity': quantity,
                        'price': book.Price
                    })
                except Book.DoesNotExist:
                    continue
        else:
            # Create order from explicit items
            items_data = data['items']
        
        if not items_data:
            return Response(
                {"error": "No valid items to order"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total and validate stock
        total_amount = Decimal('0.00')
        validated_items = []
        
        for item in items_data:
            try:
                book = Book.objects.get(BookID=item['book_id'])
                if book.Stock < item['quantity']:
                    return Response(
                        {"error": f"Not enough stock for {book.Title}. Available: {book.Stock}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                price = item.get('price', book.Price)
                subtotal = price * item['quantity']
                total_amount += subtotal
                
                validated_items.append({
                    'book': book,
                    'quantity': item['quantity'],
                    'price': price,
                    'subtotal': subtotal
                })
            except Book.DoesNotExist:
                return Response(
                    {"error": f"Book with ID {item['book_id']} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Create order
        order = Order(
            CustomerID=customer_id,
            OrderDate=timezone.now(),
            TotalAmount=total_amount,
            Status='pending'
        )
        order.save()
        
        # Create order details
        order_details = []
        for item in validated_items:
            detail = OrderDetail(
                OrderID=order.OrderID,
                BookID=item['book'].BookID,
                Quantity=item['quantity'],
                Price=item['price']
            )
            detail.save()
            order_details.append({
                'order_detail_id': detail.OrderDetailID,
                'book_id': item['book'].BookID,
                'book_title': item['book'].Title,
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': item['subtotal']
            })
        
        # Clear cart if order was created from cart
        if data.get('from_cart', True):
            request.session.pop('cart', None)
            request.session.modified = True
        
        # Return order data
        order_data = {
            'order_id': order.OrderID,
            'customer_id': order.CustomerID,
            'order_date': order.OrderDate,
            'total_amount': order.TotalAmount,
            'status': order.Status,
            'items': order_details
        }
        
        response_serializer = OrderResponseSerializer(order_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["orders"],
    responses={200: OrderListSerializer(many=True)}
)
@api_view(['GET'])
def list_orders(request):
    """List user's orders"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    orders = Order.objects.filter(CustomerID=customer_id).order_by('-OrderDate')
    
    orders_data = []
    for order in orders:
        # Count total items
        total_items = OrderDetail.objects.filter(OrderID=order.OrderID).count()
        
        orders_data.append({
            'order_id': order.OrderID,
            'order_date': order.OrderDate,
            'total_amount': order.TotalAmount,
            'status': order.Status,
            'total_items': total_items
        })
    
    serializer = OrderListSerializer(orders_data, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["orders"],
    responses={200: OrderResponseSerializer}
)
@api_view(['GET'])
def get_order(request, order_id):
    """Get order details"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        order = Order.objects.get(OrderID=order_id, CustomerID=customer_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get order details
    details = OrderDetail.objects.filter(OrderID=order.OrderID)
    order_items = []
    
    for detail in details:
        try:
            book = Book.objects.get(BookID=detail.BookID)
            book_title = book.Title
        except Book.DoesNotExist:
            book_title = f"Book ID {detail.BookID}"
        
        order_items.append({
            'order_detail_id': detail.OrderDetailID,
            'book_id': detail.BookID,
            'book_title': book_title,
            'quantity': detail.Quantity,
            'price': detail.Price,
            'subtotal': detail.Price * detail.Quantity
        })
    
    order_data = {
        'order_id': order.OrderID,
        'customer_id': order.CustomerID,
        'order_date': order.OrderDate,
        'total_amount': order.TotalAmount,
        'status': order.Status,
        'items': order_items
    }
    
    serializer = OrderResponseSerializer(order_data)
    return Response(serializer.data)


@extend_schema(
    tags=["orders"],
    request=UpdateOrderStatusSerializer,
    responses={200: OrderResponseSerializer}
)
@api_view(['PATCH'])
def cancel_order(request, order_id):
    """Cancel an order (only if pending/confirmed)"""
    customer_id = require_customer_session(request)
    if not customer_id:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        order = Order.objects.get(OrderID=order_id, CustomerID=customer_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if order.Status not in ['pending', 'confirmed']:
        return Response(
            {"error": f"Cannot cancel order with status: {order.Status}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.Status = 'cancelled'
    order.save()
    
    return Response({"message": "Order cancelled successfully"})
