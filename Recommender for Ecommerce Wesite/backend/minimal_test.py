import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

import requests
import time

def test_api():
    print("🔍 Testing API endpoints...")
    
    # Test 1: Basic connectivity
    try:
        response = requests.get("http://127.0.0.1:8000/api/schema/", timeout=10)
        print(f"✅ Schema endpoint: {response.status_code}")
        if response.status_code == 200:
            schema = response.json()
            print(f"   Schema has {len(schema.get('paths', {}))} endpoints")
    except Exception as e:
        print(f"❌ Schema endpoint failed: {e}")
        return
    
    # Test 2: User registration
    user_data = {
        "full_name": "Test User API",
        "email": "testapi@example.com", 
        "password": "testpass123",
        "phone": "1234567890"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/users/register/", json=user_data, timeout=10)
        print(f"✅ Registration endpoint: {response.status_code}")
        if response.status_code in [200, 201]:
            data = response.json()
            if 'token' in data:
                access_token = data['token']['access']
                print(f"   JWT token received (length: {len(access_token)})")
                
                # Test 3: /me endpoint with JWT
                headers = {"Authorization": f"Bearer {access_token}"}
                me_response = requests.get("http://127.0.0.1:8000/api/v1/users/me/", headers=headers, timeout=10)
                print(f"✅ JWT /me endpoint: {me_response.status_code}")
                if me_response.status_code == 200:
                    user_info = me_response.json()
                    print(f"   User: {user_info.get('full_name')}")
            else:
                print("   ⚠️  No token in registration response")
        else:
            print(f"   Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    
    print("🎯 API test completed!")

if __name__ == "__main__":
    test_api()
