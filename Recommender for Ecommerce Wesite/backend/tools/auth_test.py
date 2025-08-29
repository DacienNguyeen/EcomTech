#!/usr/bin/env python3
"""
Test script to verify registration and login functionality
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

def test_registration():
    """Test user registration"""
    print("=== Testing Registration ===")
    
    registration_data = {
        "full_name": "Test User",
        "email": "testuser@example.com", 
        "password": "securepass123",
        "phone": "0123456789",
        "address": "123 Test Street"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/users/register/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return response.json()
        else:
            print("❌ Registration failed!")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login(email="testuser@example.com", password="securepass123"):
    """Test user login"""
    print("=== Testing Login ===")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        session = requests.Session()
        response = session.post(
            f"{API_BASE}/users/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return session, response.json()
        else:
            print("❌ Login failed!")
            return None, None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, None

def test_authenticated_endpoint(session):
    """Test accessing an authenticated endpoint"""
    print("=== Testing Authenticated Endpoint ===")
    
    order_data = {
        "customer_name": "Test Customer",
        "items": [{"name": "Test Product", "price": 100000, "quantity": 1}],
        "total_amount": 100000,
        "status": "pending"
    }
    
    try:
        response = session.post(
            f"{API_BASE}/orders/",
            json=order_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Order Creation Status: {response.status_code}")
        print(f"Order Creation Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Authenticated request successful!")
            return True
        else:
            print("❌ Authenticated request failed!")
            return False
            
    except Exception as e:
        print(f"❌ Authenticated request error: {e}")
        return False

def main():
    print("🧪 Testing Registration and Login System\n")
    
    # Test registration
    reg_result = test_registration()
    
    if reg_result:
        print(f"\n📧 User created with email: {reg_result.get('user', {}).get('email')}")
        
        # Test login
        session, login_result = test_login()
        
        if session and login_result:
            print(f"👤 Logged in as: {login_result.get('user', {}).get('full_name')}")
            
            # Test authenticated endpoint
            test_authenticated_endpoint(session)
        else:
            print("⚠️  Login failed, cannot test authenticated endpoints")
    else:
        print("⚠️  Registration failed, cannot test login")
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    main()
