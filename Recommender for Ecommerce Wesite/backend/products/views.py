from rest_framework import viewsets
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
