#!/usr/bin/env python3
"""
Quick payment test to debug session issue
"""
import requests
from datetime import datetime

BASE = "http://127.0.0.1:8000"
s = requests.Session()

def main():
    print('\n== Payment Test ==')
    
    # Register and login
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    user = {
        "full_name": f"Payment Test {ts}",
        "email": f"paytest_{ts}@example.com",
        "password": "testpass123"
    }
    
    # Register
    r = s.post(f"{BASE}/api/v1/users/register/", json=user)
    print(f"Register: {r.status_code}")
    
    # Login
    r = s.post(f"{BASE}/api/v1/users/login/", json={"email": user['email'], "password": user['password']})
    print(f"Login: {r.status_code}")
    if r.status_code == 200:
        print(f"Login response: {r.json()}")
    
    # Add to cart
    r = s.post(f"{BASE}/api/v1/cart/add/", json={"book_id": 1, "quantity": 1})
    print(f"Add to cart: {r.status_code}")
    
    # Create order
    r = s.post(f"{BASE}/api/v1/orders/", json={"from_cart": True, "shipping_address": "123 Test"})
    print(f"Create order: {r.status_code}")
    if r.status_code in [200, 201]:
        order_data = r.json()
        print(f"Order created: {order_data}")
        order_id = order_data.get('order_id')
        
        if order_id:
            # Try payment
            payment_data = {
                "order_id": order_id,
                "payment_method": "credit_card",
                "card_number": "4111111111111111",
                "card_holder": "Test User"
            }
            r = s.post(f"{BASE}/api/v1/payments/charge/", json=payment_data)
            print(f"Payment: {r.status_code}")
            print(f"Payment response: {r.text[:500]}")
    else:
        print(f"Order failed: {r.text[:200]}")

if __name__ == '__main__':
    main()
