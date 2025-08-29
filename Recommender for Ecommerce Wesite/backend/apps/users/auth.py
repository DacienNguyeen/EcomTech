from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from apps.users.jwt import decode
from apps.users.models import Customer


class CustomerPrincipal:
    def __init__(self, customer_id, email=None):
        self.id = int(customer_id)
        self.email = email
        self.is_authenticated = True

    def __str__(self):
        return f"CustomerPrincipal({self.id})"


class JWTAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth.startswith(self.keyword):
            return None
        token = auth.split(' ', 1)[1]
        try:
            payload = decode(token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid or expired token')

        if payload.get('type') != 'access':
            raise exceptions.AuthenticationFailed('Not an access token')

        cid = payload.get('sub')
        if cid is None:
            raise exceptions.AuthenticationFailed('Invalid token payload')

        try:
            cust = Customer.objects.get(CustomerID=cid)
        except Customer.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        principal = CustomerPrincipal(customer_id=cid, email=payload.get('email'))
        return (principal, token)
