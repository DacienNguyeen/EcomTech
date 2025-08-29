from django.urls import path
from .views import create_order, list_orders, get_order, cancel_order

urlpatterns = [
    path('', create_order, name='create-order'),  # POST to create
    path('list/', list_orders, name='list-orders'),  # GET user orders
    path('<int:order_id>/', get_order, name='get-order'),  # GET order details
    path('<int:order_id>/cancel/', cancel_order, name='cancel-order'),  # PATCH to cancel
]
