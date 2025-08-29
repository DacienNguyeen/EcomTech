from django.urls import path
from .views import charge_payment, get_payment_status, get_order_payment

urlpatterns = [
    path('charge/', charge_payment, name='charge-payment'),
    path('<int:payment_id>/status/', get_payment_status, name='payment-status'),
    path('order/<int:order_id>/', get_order_payment, name='order-payment'),
]
