#!/usr/bin/env python3
"""
Sandbox Payment Test with Authentication
Tests the complete payment flow with proper login authentication.

Usage: python scripts/sandbox_test.py
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_USER = {
    "full_name": "Test User",
    "email": "testuser@example.com", 
    "password": "testpass123",
    "phone": "0123456789",
    "address": "123 Test Street"
}

# Global session and auth state
session = requests.Session()
access_token = None
test_results = []

def log_result(test_name, success, message, response=None):
    """Log test result with details"""
    status_code = response.status_code if response else "N/A"
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    result = {
        'test': test_name,
        'success': success,
        'message': message,
        'status_code': status_code,
        'timestamp': timestamp
    }
    test_results.append(result)
    
    status_icon = "✅" if success else "❌"
    print(f"{status_icon} [{timestamp}] {test_name}")
    print(f"   Status: {status_code} | {message}")
    
    if response and not success:
        try:
            error_body = response.json()
            print(f"   Error: {json.dumps(error_body, indent=2)[:200]}...")
        except:
            print(f"   Raw response: {response.text[:200]}...")
    print()

def get_access_token():
    """Get JWT access token from login"""
    global access_token
    try:
        # First try to register (in case user doesn't exist)
        register_response = session.post(
            f"{BASE_URL}/users/register/",
            json=TEST_USER,
            timeout=10
        )
        
        if register_response.status_code == 201:
            log_result("User Registration", True, "New user created successfully", register_response)
        elif register_response.status_code == 400:
            log_result("User Registration", True, "User already exists (expected)", register_response)
        else:
            log_result("User Registration", False, f"Unexpected status: {register_response.status_code}", register_response)
    
    except Exception as e:
        log_result("User Registration", False, f"Registration request failed: {str(e)}")
    
    # Now login to get token and session
    try:
        login_response = session.post(
            f"{BASE_URL}/users/login/",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            },
            timeout=10
        )
        
        if login_response.status_code == 200:
            data = login_response.json()
            access_token = data.get('token')
            log_result("User Login", True, f"Login successful, token received", login_response)
            return access_token
        else:
            log_result("User Login", False, f"Login failed with status: {login_response.status_code}", login_response)
            return None
            
    except Exception as e:
        log_result("User Login", False, f"Login request failed: {str(e)}")
        return None

def attach_auth_headers():
    """Get headers with authentication"""
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Add JWT token if available (preferred)
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    
    return headers

def test_authenticated_api():
    """Test API calls that require authentication"""
    
    # Test 1: Get user profile to verify auth works
    try:
        headers = attach_auth_headers()
        me_response = session.get(f"{BASE_URL}/users/me/", headers=headers, timeout=10)
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            if user_data and user_data.get('email'):
                log_result("Get User Profile", True, f"Authenticated as {user_data.get('email')}", me_response)
            else:
                log_result("Get User Profile", False, "No user data in response", me_response)
        else:
            log_result("Get User Profile", False, f"Profile check failed", me_response)
            
    except Exception as e:
        log_result("Get User Profile", False, f"Profile request failed: {str(e)}")
    
    # Test 2: Create Order (requires authentication)
    try:
        headers = attach_auth_headers()
        # Backend expects items to include book_id and quantity; use a sample book id 1 for tests
        order_data = {
            "from_cart": False,  # Use explicit items instead of session cart
            "items": [
                {
                    "book_id": 1,
                    "quantity": 1
                }
            ]
        }

        order_response = session.post(f"{BASE_URL}/orders/", json=order_data, headers=headers, timeout=10)
        
        if order_response.status_code == 201:
            order_data = order_response.json()
            order_id = order_data.get('order_id')
            log_result("Create Order API", True, f"Order created with ID: {order_id}", order_response)
            return order_id
        else:
            log_result("Create Order API", False, f"Order creation failed", order_response)
            return None
            
    except Exception as e:
        log_result("Create Order API", False, f"Order request failed: {str(e)}")
        return None

def test_payment_success(order_id):
    """Test successful payment processing"""
    if not order_id:
        log_result("Payment Success Test", False, "No order_id provided")
        return None
        
    try:
        headers = attach_auth_headers()
        payment_data = {
            "order_id": order_id,
            "payment_method": "credit_card",
            "card_number": "4111111111111111",  # Success test card
            "card_holder": "Test User",
            "card_expiry": "12/2025",
            "card_cvv": "123"
        }
        
        payment_response = session.post(
            f"{BASE_URL}/payments/charge/",
            json=payment_data,
            headers=headers,
            timeout=15
        )
        
        if payment_response.status_code == 200:
            payment_data = payment_response.json()
            payment_id = payment_data.get('payment_id')
            log_result("Payment Success Test", True, f"Payment successful, ID: {payment_id}", payment_response)
            return payment_id
        else:
            log_result("Payment Success Test", False, f"Payment failed", payment_response)
            return None
            
    except Exception as e:
        log_result("Payment Success Test", False, f"Payment request failed: {str(e)}")
        return None

def test_payment_decline():
    """Test payment decline flow with proper authentication"""
    
    # Step 1: Create order for decline test
    try:
        headers = attach_auth_headers()
        decline_order_data = {
            "from_cart": False,  # Use explicit items instead of session cart
            "items": [
                {"book_id": 1, "quantity": 1}
            ]
        }

        decline_order_response = session.post(f"{BASE_URL}/orders/", json=decline_order_data, headers=headers, timeout=10)
        
        if decline_order_response.status_code != 201:
            log_result("Decline Test - Create Order", False, f"Order creation for decline test failed", decline_order_response)
            return
            
        decline_order_id = decline_order_response.json().get('order_id')
        log_result("Decline Test - Create Order", True, f"Decline test order created: {decline_order_id}", decline_order_response)
        
    except Exception as e:
        log_result("Decline Test - Create Order", False, f"Decline order creation failed: {str(e)}")
        return
    
    # Step 2: Attempt payment with decline card
    try:
        headers = attach_auth_headers()
        decline_payment_data = {
            "order_id": decline_order_id,
            "payment_method": "credit_card",
            "card_number": "4000000000000002",  # Generic decline test card
            "card_holder": "Decline Test User",
            "card_expiry": "12/2025", 
            "card_cvv": "123"
        }
        
        decline_payment_response = session.post(
            f"{BASE_URL}/payments/charge/",
            json=decline_payment_data,
            headers=headers,
            timeout=15
        )
        
        # Check payment result - sandbox returns 200 with success=false for declines
        if decline_payment_response.status_code == 401:
            log_result("Decline Test API", False, "❌ AUTHENTICATION FAILED - Should not get 401 after login!", decline_payment_response)
        elif decline_payment_response.status_code == 200:
            try:
                decline_data = decline_payment_response.json()
                payment_success = decline_data.get('success')
                payment_status = decline_data.get('status', '')
                
                # Check if payment actually failed (sandbox behavior)
                if payment_success is False or payment_status in ['failed', 'declined']:
                    log_result("Decline Test API", True, "✅ Card properly declined as expected", decline_payment_response)
                elif 'decline' in str(decline_data).lower() or 'card_declined' in str(decline_data).lower():
                    log_result("Decline Test API", True, "✅ Card declined (found decline in response)", decline_payment_response)
                else:
                    log_result("Decline Test API", False, "⚠️  Payment succeeded when it should have been declined", decline_payment_response)
            except:
                log_result("Decline Test API", False, "Could not parse payment response", decline_payment_response)
        elif decline_payment_response.status_code in [400, 402]:
            log_result("Decline Test API", True, f"Payment declined with HTTP status {decline_payment_response.status_code}", decline_payment_response)
        else:
            log_result("Decline Test API", False, f"Unexpected status code: {decline_payment_response.status_code}", decline_payment_response)
            
    except Exception as e:
        log_result("Decline Test API", False, f"Decline payment request failed: {str(e)}")

def test_sandbox_info():
    """Test sandbox info endpoint (no auth required)"""
    try:
        info_response = session.get(f"{BASE_URL}/payments/sandbox/info/", timeout=10)
        
        if info_response.status_code == 200:
            info_data = info_response.json()
            sandbox_mode = info_data.get('sandbox_mode', False)
            test_cards_count = len(info_data.get('test_cards', {}).get('success_cards', []))
            log_result("Sandbox Info API", True, f"Sandbox mode: {sandbox_mode}, {test_cards_count} test cards", info_response)
        else:
            log_result("Sandbox Info API", False, f"Failed to get sandbox info", info_response)
            
    except Exception as e:
        log_result("Sandbox Info API", False, f"Sandbox info request failed: {str(e)}")

def print_summary():
    """Print test results summary"""
    print("\n" + "="*60)
    print("🧪 SANDBOX TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in test_results if r['success'])
    failed = len(test_results) - passed
    
    print(f"Total Tests: {len(test_results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print()
    
    # Show failed tests
    failed_tests = [r for r in test_results if not r['success']]
    if failed_tests:
        print("❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"   • {test['test']}: {test['message']}")
        print()
    
    # Show critical auth issues
    auth_failures = [r for r in test_results if not r['success'] and '401' in str(r['status_code'])]
    if auth_failures:
        print("🚨 AUTHENTICATION ISSUES:")
        for test in auth_failures:
            print(f"   • {test['test']}: Status {test['status_code']}")
        print("   → Check login flow and session/JWT token handling")
        print()
    
    success_rate = (passed / len(test_results)) * 100 if test_results else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 All tests passed! Payment sandbox is working correctly.")
    elif success_rate >= 80:
        print("⚠️  Most tests passed, but some issues detected.")
    else:
        print("🔴 Multiple failures detected. Check authentication and API setup.")

def main():
    """Run all sandbox tests with authentication"""
    print("🚀 Starting Authenticated Sandbox Payment Tests")
    print(f"Backend URL: {BASE_URL}")
    print(f"Test User: {TEST_USER['email']}")
    print("-" * 60)
    
    # Step 1: Get authentication token
    if not get_access_token():
        print("❌ Failed to authenticate. Cannot proceed with tests.")
        return
    
    # Step 2: Test endpoints that don't require auth
    test_sandbox_info()
    
    # Step 3: Test authenticated endpoints 
    test_authenticated_api()
    
    # Step 4: Test payment flows
    order_id = test_authenticated_api()  # This returns order_id if successful
    if order_id:
        payment_id = test_payment_success(order_id)
    
    # Step 5: Test decline scenario
    test_payment_decline()
    
    # Step 6: Print summary
    print_summary()

if __name__ == "__main__":
    main()
