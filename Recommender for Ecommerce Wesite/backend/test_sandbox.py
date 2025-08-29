#!/usr/bin/env python3
"""
Payment Sandbox Test Script
Demonstrates sandbox payment functionality with test cards and scenarios
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_payment_sandbox():
    """Test the payment sandbox functionality"""
    print("💳 Payment Sandbox Test Suite")
    print("=" * 60)
    
    # Step 1: Get sandbox info
    print("\n1. Getting sandbox information...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/payments/sandbox/info/")
        if response.status_code == 200:
            sandbox_info = response.json()
            print(f"✅ Sandbox Mode: {sandbox_info['sandbox_mode']}")
            print(f"✅ Supported Methods: {', '.join(sandbox_info['supported_methods'])}")
            print(f"✅ Test Cards Available: {len(sandbox_info['test_cards']['success_cards'])} success cards")
            print(f"✅ Webhook URL: {sandbox_info.get('webhook_url', 'N/A')}")
        else:
            print(f"❌ Failed to get sandbox info: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting sandbox info: {e}")
        return
    
    # For testing, we need to simulate a user session and order
    # In a real test, you would:
    # 1. Register/login a user
    # 2. Add items to cart  
    # 3. Create an order
    # 4. Then test payment
    
    print("\n📋 Available Test Scenarios:")
    test_scenarios = [
        {
            'name': 'Successful Credit Card Payment',
            'card_number': '4111111111111111',
            'expected': 'success'
        },
        {
            'name': 'Declined Credit Card Payment', 
            'card_number': '4000000000000002',
            'expected': 'decline'
        },
        {
            'name': 'PayPal Payment',
            'method': 'paypal',
            'expected': 'success'
        },
        {
            'name': 'Bank Transfer Payment',
            'method': 'bank_transfer', 
            'expected': 'processing'
        },
        {
            'name': 'E-Wallet Payment',
            'method': 'e_wallet',
            'expected': 'success'
        },
        {
            'name': 'Cash on Delivery',
            'method': 'cash_on_delivery',
            'expected': 'pending'
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"{i}. {scenario['name']} - Expected: {scenario['expected']}")
    
    print(f"\n🧪 To test payments manually:")
    print(f"1. Start Django server: python manage.py runserver")
    print(f"2. Visit Swagger UI: {BASE_URL}/api/docs/")
    print(f"3. Register/login a user")
    print(f"4. Create an order")
    print(f"5. Use POST /api/v1/payments/charge/ with test data")
    
    print(f"\n📖 Test Card Numbers:")
    print(f"• Success: 4111111111111111 (Visa)")
    print(f"• Success: 5555555555554444 (Mastercard)")  
    print(f"• Decline: 4000000000000002 (Generic decline)")
    print(f"• Decline: 4000000000000069 (Expired card)")
    print(f"• Special: 4000000000000341 (Requires 3D Secure)")
    
    print(f"\n💡 Payment Methods:")
    for method in sandbox_info['supported_methods']:
        print(f"• {method}")
        
    print(f"\n🔗 API Endpoints:")
    print(f"• POST /api/v1/payments/charge/ - Process payment")
    print(f"• GET /api/v1/payments/<id>/status/ - Check payment status")
    print(f"• GET /api/v1/payments/order/<id>/ - Get order payment")
    print(f"• GET /api/v1/payments/sandbox/info/ - Sandbox information")
    print(f"• POST /api/v1/payments/sandbox/webhook/<id>/ - Simulate webhook")
    
    print(f"\n🎯 Sandbox Features:")
    print(f"• Realistic payment processing simulation")
    print(f"• Test card validation and behavior")
    print(f"• Processing delays simulation")
    print(f"• Multiple payment methods support")
    print(f"• Webhook event simulation")
    print(f"• Detailed error codes and messages")

if __name__ == "__main__":
    test_payment_sandbox()
