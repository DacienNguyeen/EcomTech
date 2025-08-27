from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from ...models import Customer
from .serializers import RegisterInSerializer, LoginInSerializer, CustomerOutSerializer, UserSerializer

User = get_user_model()


@extend_schema(request=RegisterInSerializer, responses={201: CustomerOutSerializer})
@api_view(['POST'])
def register(request):
    serializer = RegisterInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    cust = serializer.create(serializer.validated_data)
    out = CustomerOutSerializer(cust)
    return Response(out.data, status=status.HTTP_201_CREATED)


@extend_schema(request=LoginInSerializer, responses={200: OpenApiResponse(response=CustomerOutSerializer)})
@api_view(['POST'])
def login_view(request):
    serializer = LoginInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        cust = Customer.objects.get(Email=data['email'])
    except Customer.DoesNotExist:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(data['password'], cust.PasswordHash):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # ensure session exists
    if not request.session.session_key:
        request.session.create()
    request.session['customer_id'] = cust.CustomerID
    out = CustomerOutSerializer(cust)
    return Response(out.data)


@extend_schema(responses={204: OpenApiResponse(description='No Content')})
@api_view(['POST'])
def logout_view(request):
    try:
        del request.session['customer_id']
    except KeyError:
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses={200: CustomerOutSerializer, 204: OpenApiResponse(description='No user in session')})
@api_view(['GET'])
def me(request):
    cid = request.session.get('customer_id')
    if not cid:
        return Response(None, status=status.HTTP_200_OK)
    try:
        cust = Customer.objects.get(CustomerID=cid)
    except Customer.DoesNotExist:
        return Response(None, status=status.HTTP_200_OK)
    out = CustomerOutSerializer(cust)
    return Response(out.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
