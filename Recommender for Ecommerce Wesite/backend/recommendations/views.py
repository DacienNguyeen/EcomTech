from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer

class RecommendationView(APIView):
	def get(self, request, format=None):
		# Gợi ý sản phẩm đơn giản: lấy 5 sản phẩm mới nhất
		products = Product.objects.order_by('-created_at')[:5]
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)

# Views for recommender app
from django.shortcuts import render

# Create your views here.
