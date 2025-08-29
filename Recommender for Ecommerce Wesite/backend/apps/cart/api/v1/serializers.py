from rest_framework import serializers
from apps.catalog.models import Book


class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    def validate_book_id(self, value):
        try:
            Book.objects.get(BookID=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value


class CartItemResponseSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartResponseSerializer(serializers.Serializer):
    items = CartItemResponseSerializer(many=True)
    total_items = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    def validate_book_id(self, value):
        try:
            book = Book.objects.get(BookID=value)
            if book.Stock < 1:
                raise serializers.ValidationError("Book out of stock")
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)  # 0 means remove
