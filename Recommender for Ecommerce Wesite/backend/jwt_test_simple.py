#!/usr/bin/env python3
"""
Simple JWT Authentication Test
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_jwt_auth():
    print("🔐 JWT Authentication Test")
    print("="*50)
    
    # Test user data
    timestamp = datetime.now().strftime('%H%M%S')
    test_user = {
        "full_name": f"Test User {timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpass123",
        "phone": "1234567890",
        "address": "123 Test Street"
    }
    
    session = requests.Session()
    
    # 1. Register user
    print("1. Testing user registration...")
    try:
        response = session.post(f"{BASE_URL}/api/v1/users/register/", json=test_user)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"   ✅ Registration successful")
            print(f"   User ID: {data.get('user', {}).get('customer_id')}")
            if 'token' in data:
                print(f"   🔑 Access token received (length: {len(data['token']['access'])})")
                access_token = data['token']['access']
            else:
                print("   ⚠️  No token in response")
                return
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 2. Login user
    print("\n2. Testing user login...")
    try:
        login_data = {"email": test_user["email"], "password": test_user["password"]}
        response = session.post(f"{BASE_URL}/api/v1/users/login/", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful")
            if 'token' in data:
                print(f"   🔑 New access token received")
                access_token = data['token']['access']
            else:
                print("   ⚠️  No token in login response")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 3. Test /me endpoint with JWT
    print("\n3. Testing /me endpoint with JWT...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/users/me/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ JWT authentication working")
            print(f"   User: {data.get('full_name')} ({data.get('email')})")
        else:
            print(f"   ❌ JWT auth failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Test protected endpoint (activities)
    print("\n4. Testing protected activities endpoint...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        activity_data = {
            "activity_type": "test",
            "description": "JWT test activity"
        }
        response = requests.post(f"{BASE_URL}/api/v1/activities/", json=activity_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"   ✅ Protected endpoint accessible with JWT")
        else:
            print(f"   ❌ Protected endpoint failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Test cart endpoint
    print("\n5. Testing cart endpoint...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/cart/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Cart accessible")
            print(f"   Total items: {data.get('total_items', 0)}")
        else:
            print(f"   ❌ Cart access failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 JWT Test completed!")

if __name__ == "__main__":
    test_jwt_auth()
