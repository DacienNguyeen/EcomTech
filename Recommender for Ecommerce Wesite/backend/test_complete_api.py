#!/usr/bin/env python3
"""
Complete API Test Suite for Activities and Authentication
Tests all endpoints: schema, auth flow, activities (single + bulk)
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
    print_section("🧪 COMPLETE API TEST SUITE")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Schema endpoint
    print_section("1. OPENAPI SCHEMA TEST")
    try:
        response = session.get(f"{BASE_URL}/api/schema/?format=json")
        if response.status_code == 200:
            schema = response.json()
            activities_found = any("activities" in path for path in schema.get("paths", {}).keys())
            test_result("Schema endpoint accessible", True, f"Status: {response.status_code}")
            test_result("Activities endpoints in schema", activities_found, 
                       f"Found paths: {list(schema.get('paths', {}).keys())}")
        else:
            test_result("Schema endpoint accessible", False, f"Status: {response.status_code}")
    except Exception as e:
        test_result("Schema endpoint accessible", False, f"Error: {e}")
    
    # Test 2: Unauthorized access test
    print_section("2. UNAUTHORIZED ACCESS TEST")
    try:
        response = session.post(f"{BASE_URL}/api/v1/activities/", 
                               json={"action": "view", "book_id": 1})
        test_result("Unauthorized access blocked", response.status_code == 401, 
                   f"Status: {response.status_code}")
    except Exception as e:
        test_result("Unauthorized access blocked", False, f"Error: {e}")
    
    # Test 3: User registration
    print_section("3. USER REGISTRATION TEST")
    test_user = {
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/v1/users/register/", json=test_user)
        if response.status_code in [200, 201]:
            test_result("User registration", True, f"Status: {response.status_code}")
            registration_success = True
        else:
            test_result("User registration", False, 
                       f"Status: {response.status_code}, Response: {response.text}")
            registration_success = False
    except Exception as e:
        test_result("User registration", False, f"Error: {e}")
        registration_success = False
    
    # Test 4: User login
    print_section("4. USER LOGIN TEST")
    if registration_success:
        try:
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            response = session.post(f"{BASE_URL}/api/v1/users/login/", json=login_data)
            if response.status_code == 200:
                test_result("User login", True, f"Status: {response.status_code}")
                login_success = True
            else:
                test_result("User login", False, 
                           f"Status: {response.status_code}, Response: {response.text}")
                login_success = False
        except Exception as e:
            test_result("User login", False, f"Error: {e}")
            login_success = False
    else:
        test_result("User login", False, "Skipped due to registration failure")
        login_success = False
    
    # Test 5: Single activity creation
    print_section("5. SINGLE ACTIVITY TEST")
    if login_success:
        try:
            activity_data = {
                "action": "view",
                "book_id": 1
            }
            response = session.post(f"{BASE_URL}/api/v1/activities/", json=activity_data)
            if response.status_code in [200, 201]:
                result = response.json()
                test_result("Single activity creation", True, 
                           f"Status: {response.status_code}, Activity ID: {result.get('activity_id')}")
            else:
                test_result("Single activity creation", False, 
                           f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            test_result("Single activity creation", False, f"Error: {e}")
    else:
        test_result("Single activity creation", False, "Skipped due to login failure")
    
    # Test 6: Bulk activity creation
    print_section("6. BULK ACTIVITY TEST")
    if login_success:
        try:
            bulk_data = {
                "activities": [
                    {"action": "view", "book_id": 1},
                    {"action": "add_to_cart", "book_id": 2},
                    {"action": "purchase", "book_id": 3}
                ]
            }
            response = session.post(f"{BASE_URL}/api/v1/activities/bulk/", json=bulk_data)
            if response.status_code in [200, 201]:
                result = response.json()
                test_result("Bulk activity creation", True, 
                           f"Status: {response.status_code}, Created: {result.get('created_count', 0)} activities")
            else:
                test_result("Bulk activity creation", False, 
                           f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            test_result("Bulk activity creation", False, f"Error: {e}")
    else:
        test_result("Bulk activity creation", False, "Skipped due to login failure")
    
    # Test 7: User info endpoint
    print_section("7. USER INFO TEST")
    if login_success:
        try:
            response = session.get(f"{BASE_URL}/api/v1/users/me/")
            if response.status_code == 200:
                user_info = response.json()
                test_result("User info retrieval", True, 
                           f"Status: {response.status_code}, User: {user_info.get('username')}")
            else:
                test_result("User info retrieval", False, 
                           f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            test_result("User info retrieval", False, f"Error: {e}")
    else:
        test_result("User info retrieval", False, "Skipped due to login failure")
    
    print_section("🎯 TEST SUMMARY")
    print("✅ All tests completed! Check results above.")
    print("📋 Next steps:")
    print("   1. Open Swagger UI at: http://127.0.0.1:8000/api/docs/")
    print("   2. Test endpoints manually in Swagger interface")
    print("   3. Verify Activities endpoints are visible and documented")

if __name__ == "__main__":
    main()
