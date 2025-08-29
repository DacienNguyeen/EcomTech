from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from decimal import Decimal

from apps.catalog.models import Book
from .serializers import (
    CartResponseSerializer, 
    AddToCartSerializer, 
    UpdateCartItemSerializer,
    CartItemResponseSerializer
)


def get_cart_from_session(request):
    """Get cart items from session"""
    return request.session.get('cart', {})


def save_cart_to_session(request, cart):
    """Save cart items to session"""
    request.session['cart'] = cart
    request.session.modified = True


def calculate_cart_data(cart_items):
    """Calculate cart totals and get book details"""
    items = []
    total_amount = Decimal('0.00')
    total_items = 0
    
    for book_id_str, quantity in cart_items.items():
        try:
            book = Book.objects.get(BookID=int(book_id_str))
            subtotal = book.Price * quantity
            total_amount += subtotal
            total_items += quantity
            
            items.append({
                'book_id': book.BookID,
                'title': book.Title,
                'price': book.Price,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Book.DoesNotExist:
            continue  # Skip invalid books
    
    return {
        'items': items,
        'total_items': total_items,
        'total_amount': total_amount
    }


@extend_schema(
    tags=["cart"],
    responses={200: CartResponseSerializer}
)
@api_view(['GET'])
def get_cart(request):
    """Get current cart contents"""
    cart_items = get_cart_from_session(request)
    cart_data = calculate_cart_data(cart_items)
    
    serializer = CartResponseSerializer(cart_data)
    return Response(serializer.data)


@extend_schema(
    tags=["cart"],
    request=AddToCartSerializer,
    responses={200: CartResponseSerializer}
)
@api_view(['POST'])
def add_to_cart(request):
    """Add item to cart"""
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        cart_items = get_cart_from_session(request)
        book_id_str = str(book_id)
        
        # Check stock
        try:
            book = Book.objects.get(BookID=book_id)
            current_quantity = cart_items.get(book_id_str, 0)
            new_quantity = current_quantity + quantity
            
            if book.Stock < new_quantity:
                return Response(
                    {"error": f"Not enough stock. Available: {book.Stock}, Requested: {new_quantity}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add to cart
        cart_items[book_id_str] = new_quantity
        save_cart_to_session(request, cart_items)
        
        # Return updated cart
        cart_data = calculate_cart_data(cart_items)
        response_serializer = CartResponseSerializer(cart_data)
        return Response(response_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["cart"],
    request=UpdateCartItemSerializer,
    responses={200: CartResponseSerializer}
)
@api_view(['PATCH'])
def update_cart_item(request, book_id):
    """Update cart item quantity"""
    serializer = UpdateCartItemSerializer(data=request.data)
    if serializer.is_valid():
        quantity = serializer.validated_data['quantity']
        
        cart_items = get_cart_from_session(request)
        book_id_str = str(book_id)
        
        if quantity == 0:
            # Remove item
            cart_items.pop(book_id_str, None)
        else:
            # Check stock
            try:
                book = Book.objects.get(BookID=book_id)
                if book.Stock < quantity:
                    return Response(
                        {"error": f"Not enough stock. Available: {book.Stock}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Book.DoesNotExist:
                return Response(
                    {"error": "Book not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            cart_items[book_id_str] = quantity
        
        save_cart_to_session(request, cart_items)
        
        # Return updated cart
        cart_data = calculate_cart_data(cart_items)
        response_serializer = CartResponseSerializer(cart_data)
        return Response(response_serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["cart"],
    responses={200: CartResponseSerializer}
)
@api_view(['DELETE'])
def remove_from_cart(request, book_id):
    """Remove item from cart"""
    cart_items = get_cart_from_session(request)
    book_id_str = str(book_id)
    cart_items.pop(book_id_str, None)
    save_cart_to_session(request, cart_items)
    
    # Return updated cart
    cart_data = calculate_cart_data(cart_items)
    response_serializer = CartResponseSerializer(cart_data)
    return Response(response_serializer.data)


@extend_schema(
    tags=["cart"],
    responses={200: {"description": "Cart cleared successfully"}}
)
@api_view(['DELETE'])
def clear_cart(request):
    """Clear entire cart"""
    request.session.pop('cart', None)
    request.session.modified = True
    return Response({"message": "Cart cleared successfully"})
