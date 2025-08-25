from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_recs(request):
  return Response({'results': []})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_recs(request, user_id: int):
  return Response({'results': []})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def similar_items(request, product_id: int):
  return Response({'results': []})
