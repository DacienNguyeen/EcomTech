#!/usr/bin/env python3
"""
Complete test for Cart, Orders, and Payments APIs
Tests the full e-commerce flow: add to cart → create order → process payment
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_result(test_name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"   → {message}")

def main():
    print_section("🛒 E-COMMERCE API TEST SUITE")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Register and login first
    print_section("1. USER AUTHENTICATION")
    test_user = {
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    # Register
    try:
        response = session.post(f"{BASE_URL}/api/v1/users/register/", json=test_user)
        test_result("User registration", response.status_code in [200, 201], 
                   f"Status: {response.status_code}")
        registration_success = response.status_code in [200, 201]
    except Exception as e:
        test_result("User registration", False, f"Error: {e}")
        registration_success = False
    
    # Login
    if registration_success:
        try:
            login_data = {"username": test_user["username"], "password": test_user["password"]}
            response = session.post(f"{BASE_URL}/api/v1/users/login/", json=login_data)
            test_result("User login", response.status_code == 200, 
                       f"Status: {response.status_code}")
            login_success = response.status_code == 200
        except Exception as e:
            test_result("User login", False, f"Error: {e}")
            login_success = False
    else:
        login_success = False
    
    if not login_success:
        print("❌ Cannot continue without authentication")
        return
    
    # Test Cart API
    print_section("2. CART API TESTS")
    
    # Get empty cart
    try:
        response = session.get(f"{BASE_URL}/api/v1/cart/")
        test_result("Get empty cart", response.status_code == 200, 
                   f"Items: {response.json().get('total_items', 0)}")
    except Exception as e:
        test_result("Get empty cart", False, f"Error: {e}")
    
    # Add items to cart
    cart_items_added = []
    try:
        # Add first item
        add_data = {"book_id": 1, "quantity": 2}
        response = session.post(f"{BASE_URL}/api/v1/cart/add/", json=add_data)
        if response.status_code == 200:
            cart_data = response.json()
            test_result("Add item to cart", True, 
                       f"Total items: {cart_data.get('total_items', 0)}")
            cart_items_added.append(1)
        else:
            test_result("Add item to cart", False, f"Status: {response.status_code}")
        
        # Add second item
        add_data = {"book_id": 2, "quantity": 1}
        response = session.post(f"{BASE_URL}/api/v1/cart/add/", json=add_data)
        if response.status_code == 200:
            cart_data = response.json()
            test_result("Add second item", True, 
                       f"Total items: {cart_data.get('total_items', 0)}")
            cart_items_added.append(2)
        else:
            test_result("Add second item", False, f"Status: {response.status_code}")
            
    except Exception as e:
        test_result("Add items to cart", False, f"Error: {e}")
    
    # Update cart item
    if cart_items_added:
        try:
            update_data = {"quantity": 3}
            response = session.patch(f"{BASE_URL}/api/v1/cart/items/1/", json=update_data)
            test_result("Update cart item", response.status_code == 200, 
                       f"Status: {response.status_code}")
        except Exception as e:
            test_result("Update cart item", False, f"Error: {e}")
    
    # Test Orders API
    print_section("3. ORDERS API TESTS")
    
    order_id = None
    # Create order from cart
    try:
        order_data = {"from_cart": True, "shipping_address": "123 Test St, Test City"}
        response = session.post(f"{BASE_URL}/api/v1/orders/", json=order_data)
        if response.status_code == 201:
            order_response = response.json()
            order_id = order_response.get('order_id')
            test_result("Create order from cart", True, 
                       f"Order ID: {order_id}, Total: ${order_response.get('total_amount', 0)}")
        else:
            test_result("Create order from cart", False, 
                       f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        test_result("Create order from cart", False, f"Error: {e}")
    
    # List orders
    try:
        response = session.get(f"{BASE_URL}/api/v1/orders/list/")
        if response.status_code == 200:
            orders = response.json()
            test_result("List orders", True, 
                       f"Found {len(orders)} orders")
        else:
            test_result("List orders", False, f"Status: {response.status_code}")
    except Exception as e:
        test_result("List orders", False, f"Error: {e}")
    
    # Get order details
    if order_id:
        try:
            response = session.get(f"{BASE_URL}/api/v1/orders/{order_id}/")
            if response.status_code == 200:
                order_details = response.json()
                test_result("Get order details", True, 
                           f"Order status: {order_details.get('status')}")
            else:
                test_result("Get order details", False, f"Status: {response.status_code}")
        except Exception as e:
            test_result("Get order details", False, f"Error: {e}")
    
    # Test Payments API
    print_section("4. PAYMENTS API TESTS")
    
    payment_id = None
    if order_id:
        # Process payment
        try:
            payment_data = {
                "order_id": order_id,
                "payment_method": "credit_card",
                "card_number": "4111111111111111",
                "card_holder": "Test User"
            }
            response = session.post(f"{BASE_URL}/api/v1/payments/charge/", json=payment_data)
            if response.status_code == 200:
                payment_response = response.json()
                payment_id = payment_response.get('payment_id')
                test_result("Process payment", True, 
                           f"Payment ID: {payment_id}, Status: {payment_response.get('status')}")
            else:
                test_result("Process payment", False, 
                           f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            test_result("Process payment", False, f"Error: {e}")
        
        # Check payment status
        if payment_id:
            try:
                response = session.get(f"{BASE_URL}/api/v1/payments/{payment_id}/status/")
                if response.status_code == 200:
                    payment_status = response.json()
                    test_result("Check payment status", True, 
                               f"Status: {payment_status.get('status')}")
                else:
                    test_result("Check payment status", False, f"Status: {response.status_code}")
            except Exception as e:
                test_result("Check payment status", False, f"Error: {e}")
        
        # Get order payment info
        try:
            response = session.get(f"{BASE_URL}/api/v1/payments/order/{order_id}/")
            if response.status_code == 200:
                order_payment = response.json()
                test_result("Get order payment info", True, 
                           f"Status: {order_payment.get('status')}")
            else:
                test_result("Get order payment info", False, f"Status: {response.status_code}")
        except Exception as e:
            test_result("Get order payment info", False, f"Error: {e}")
    
    # Test error cases
    print_section("5. ERROR HANDLING TESTS")
    
    # Test unauthorized cart access (shouldn't fail - cart is session-based)
    new_session = requests.Session()
    try:
        response = new_session.get(f"{BASE_URL}/api/v1/cart/")
        test_result("Anonymous cart access", response.status_code == 200, 
                   "Anonymous users can access cart")
    except Exception as e:
        test_result("Anonymous cart access", False, f"Error: {e}")
    
    # Test unauthorized order creation
    try:
        order_data = {"from_cart": True}
        response = new_session.post(f"{BASE_URL}/api/v1/orders/", json=order_data)
        test_result("Unauthorized order creation", response.status_code == 401, 
                   "Orders require authentication")
    except Exception as e:
        test_result("Unauthorized order creation", False, f"Error: {e}")
    
    print_section("🎯 TEST SUMMARY")
    print("✅ E-commerce API tests completed!")
    print("📋 Available endpoints:")
    print("   Cart: GET,POST /api/v1/cart/, PATCH,DELETE /api/v1/cart/items/{id}/")
    print("   Orders: POST /api/v1/orders/, GET /api/v1/orders/list/, GET /api/v1/orders/{id}/")
    print("   Payments: POST /api/v1/payments/charge/, GET /api/v1/payments/{id}/status/")
    print("   Swagger UI: http://127.0.0.1:8000/api/docs/")

if __name__ == "__main__":
    main()
