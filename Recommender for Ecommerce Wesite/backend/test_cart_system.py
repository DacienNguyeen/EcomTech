import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.catalog.models import Book
from apps.orders.models import Order, OrderDetail
from apps.users.models import User

print("=== TESTING CART & ORDER SYSTEM ===")

# 1. Check books
print("\n1. Available Books:")
books = Book.objects.all()[:3]
for book in books:
    print(f"   - ID {book.BookID}: {book.Title} - ${book.Price} (Stock: {book.Stock})")

# 2. Test API endpoints via direct function calls
from apps.cart.api.v1.views import get_cart, add_to_cart
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

print("\n2. Testing Cart Functions:")

# Create a mock request
factory = RequestFactory()
request = factory.get('/cart/')
request.user = AnonymousUser()
request.session = {}
request.session.session_key = 'test_session_123'

# Test get_cart
print("   - Testing get_cart...")
try:
    response = get_cart(request)
    print(f"     Status: {response.status_code}")
    print(f"     Data: {response.data}")
except Exception as e:
    print(f"     Error: {e}")

print("\n3. Testing Add to Cart:")

# Test add_to_cart
if books:
    factory = RequestFactory()
    request = factory.post('/cart/add/', {'book_id': books[0].BookID, 'quantity': 2})
    request.user = AnonymousUser()
    request.session = {}
    request.session.session_key = 'test_session_123'
    
    try:
        response = add_to_cart(request)
        print(f"   Status: {response.status_code}")
        print(f"   Data: {response.data}")
    except Exception as e:
        print(f"   Error: {e}")

print("\n4. Check Orders table:")
cart_orders = Order.objects.filter(Status__startswith='cart')
print(f"   Found {cart_orders.count()} cart orders")
for order in cart_orders:
    print(f"   - Order {order.OrderID}: Status={order.Status}, Total=${order.TotalAmount}")
    
print("\n=== TEST COMPLETED ===")
