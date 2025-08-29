#!/usr/bin/env python3
"""
Simple Authentication Test for Payment APIs
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_basic_auth_flow():
    print("=== Testing Authentication Flow ===")
    
    # Test 1: Check if server is responding
    print("1. Testing server connection...")
    try:
        response = requests.get(f"{BASE_URL}/payments/sandbox/info/", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server responding: {response.status_code}")
            data = response.json()
            print(f"   Sandbox mode: {data.get('sandbox_mode')}")
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test 2: Registration 
    print("\n2. Testing user registration...")
    session = requests.Session()
    user_data = {
        "full_name": "Test Auth User", 
        "email": "authtest@example.com",
        "password": "testpass123",
        "phone": "0987654321",
        "address": "Test Address"
    }
    
    try:
        reg_response = session.post(f"{BASE_URL}/users/register/", json=user_data, timeout=10)
        print(f"   Registration response: {reg_response.status_code}")
        if reg_response.status_code in [200, 201]:
            print("✅ Registration successful")
            reg_data = reg_response.json()
            print(f"   User created: {reg_data.get('user', {}).get('email', 'N/A')}")
        elif reg_response.status_code == 400:
            print("✅ User already exists (expected)")
        else:
            print(f"❌ Registration failed: {reg_response.text[:200]}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 3: Login
    print("\n3. Testing login...")
    try:
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_response = session.post(f"{BASE_URL}/users/login/", json=login_data, timeout=10)
        print(f"   Login response: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            login_resp_data = login_response.json()
            token = login_resp_data.get('token')
            print(f"   JWT token received: {'Yes' if token else 'No'}")
            print(f"   Session cookies: {len(session.cookies)} cookies")
            
            # Show cookies
            for cookie in session.cookies:
                print(f"   Cookie: {cookie.name} = {cookie.value[:20]}...")
                
        else:
            print(f"❌ Login failed: {login_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Test 4: Try authenticated endpoint
    print("\n4. Testing authenticated endpoint...")
    try:
        # Try with session cookies (Django session auth)
        me_response = session.get(f"{BASE_URL}/users/me/", timeout=10)
        print(f"   /users/me/ response: {me_response.status_code}")
        
        if me_response.status_code == 200:
            me_data = me_response.json()
            if me_data and me_data.get('email'):
                print(f"✅ Session authentication working")
                print(f"   Authenticated as: {me_data.get('email')}")
            else:
                print("⚠️  Response OK but no user data")
        else:
            print(f"❌ Authentication check failed: {me_response.text[:100]}")
            
    except Exception as e:
        print(f"❌ Auth check error: {e}")
    
    # Test 5: Try to create order (the problematic endpoint)
    print("\n5. Testing order creation (main issue)...")
    try:
        order_data = {
            "customer_name": "Auth Test User",
            "items": [{"name": "Test Item", "price": 50000, "quantity": 1}],
            "total_amount": 50000,
            "status": "pending"
        }
        
        order_response = session.post(f"{BASE_URL}/orders/", json=order_data, timeout=10)
        print(f"   Order creation response: {order_response.status_code}")
        
        if order_response.status_code == 201:
            print("✅ Order created successfully!")
            order_resp_data = order_response.json()
            order_id = order_resp_data.get('order_id')
            print(f"   Order ID: {order_id}")
        elif order_response.status_code == 401:
            print("❌ Still getting 401 - Authentication not working")
            print(f"   Response: {order_response.text[:200]}")
        else:
            print(f"⚠️  Other error: {order_response.status_code}")
            print(f"   Response: {order_response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_basic_auth_flow()
