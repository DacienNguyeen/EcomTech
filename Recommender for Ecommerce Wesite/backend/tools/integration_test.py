#!/usr/bin/env python3
"""
Lightweight integration test for local dev servers.
Exercises: register -> login -> add to cart -> create order -> charge (success & decline) -> check payment status
Prints concise PASS/FAIL lines.
"""
import requests
import time
from datetime import datetime

BASE = "http://127.0.0.1:8000"
s = requests.Session()

passed = 0
failed = 0

def ok(name, cond, msg=""):
    global passed, failed
    if cond:
        print(f"✅ {name}")
        passed += 1
    else:
        print(f"❌ {name} - {msg}")
        failed += 1


def main():
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    username = f"itest_{ts}"
    user = {
        "full_name": f"IT Test {ts}",
        "email": f"{username}@example.com",
        "password": "testpass123"
    }

    print('\n== Integration test (light) ==')
    # Register
    try:
        r = s.post(f"{BASE}/api/v1/users/register/", json=user, timeout=10)
        ok('User registration', r.status_code in (200,201), f'status={r.status_code} body={r.text[:200]}')
    except Exception as e:
        ok('User registration', False, str(e))
        print_summary(); return

    # Login
    try:
        r = s.post(f"{BASE}/api/v1/users/login/", json={"email": user['email'], "password": user['password']}, timeout=10)
        ok('User login', r.status_code == 200, f'status={r.status_code} body={r.text[:200]}')
    except Exception as e:
        ok('User login', False, str(e)); print_summary(); return

    # Get cart
    try:
        r = s.get(f"{BASE}/api/v1/cart/", timeout=10)
        ok('Get cart', r.status_code == 200, f'status={r.status_code}')
    except Exception as e:
        ok('Get cart', False, str(e))

    # Add to cart
    try:
        r = s.post(f"{BASE}/api/v1/cart/add/", json={"book_id": 1, "quantity": 1}, timeout=10)
        ok('Add to cart', r.status_code in (200,201), f'status={r.status_code} body={r.text[:200]}')
    except Exception as e:
        ok('Add to cart', False, str(e))

    # Create order
    order_id = None
    try:
        r = s.post(f"{BASE}/api/v1/orders/", json={"from_cart": True, "shipping_address": "123 Test"}, timeout=10)
        ok('Create order', r.status_code in (200,201), f'status={r.status_code} body={r.text[:200]}')
        if r.status_code in (200,201):
            try:
                jr = r.json()
                order_id = jr.get('order_id') or jr.get('OrderID') or jr.get('id')
            except Exception:
                order_id = None
    except Exception as e:
        ok('Create order', False, str(e))

    if not order_id:
        print('No order_id returned; cannot continue payments steps')
        print_summary(); return

    # Process successful payment
    payment_id = None
    try:
        payload = {
            "order_id": order_id,
            "payment_method": "credit_card",
            "card_number": "4111111111111111",
            "card_holder": "IT Test"
        }
        r = s.post(f"{BASE}/api/v1/payments/charge/", json=payload, timeout=15)
        ok('Charge (success) response code', r.status_code == 200, f'status={r.status_code} body={r.text[:200]}')
        if r.status_code == 200:
            jr = r.json()
            payment_id = jr.get('payment_id') or jr.get('paymentID') or jr.get('id')
            status = jr.get('status')
            ok('Charge (success) status', status in ('completed','processing','pending','requires_action'), f'status_field={status}')
    except Exception as e:
        ok('Charge (success)', False, str(e))

    # Check payment status
    if payment_id:
        try:
            r = s.get(f"{BASE}/api/v1/payments/{payment_id}/status/", timeout=10)
            ok('Get payment status', r.status_code == 200, f'status={r.status_code} body={r.text[:200]}')
        except Exception as e:
            ok('Get payment status', False, str(e))
    else:
        ok('Get payment status', False, 'no payment_id')

    # Create another order to test decline
    # First add item to cart again (previous order cleared it)
    try:
        r = s.post(f"{BASE}/api/v1/cart/add/", json={"book_id": 1, "quantity": 1}, timeout=10)
        ok('Add to cart (for decline test)', r.status_code in (200,201), f'status={r.status_code}')
    except Exception as e:
        ok('Add to cart (for decline test)', False, str(e))
    
    try:
        r = s.post(f"{BASE}/api/v1/orders/", json={"from_cart": True, "shipping_address": "456 Test"}, timeout=10)
        ok('Create order (for decline)', r.status_code in (200,201), f'status={r.status_code}')
        if r.status_code in (200,201):
            jr = r.json()
            decline_order_id = jr.get('order_id') or jr.get('OrderID') or jr.get('id')
        else:
            decline_order_id = None
    except Exception as e:
        ok('Create order (for decline)', False, str(e)); decline_order_id = None

    if decline_order_id:
        try:
            payload = {
                "order_id": decline_order_id,
                "payment_method": "credit_card",
                "card_number": "4000000000000002",
                "card_holder": "IT Test"
            }
            r = s.post(f"{BASE}/api/v1/payments/charge/", json=payload, timeout=15)
            # decline may return 200 with status failed, or 400/402; accept those
            ok('Charge (decline) response code', r.status_code in (200,400,402,402), f'status={r.status_code} body={r.text[:200]}')
            if r.status_code == 200:
                jr = r.json()
                status = jr.get('status')
                ok('Charge (decline) status indicates failure', status in ('failed','payment_failed'), f'status_field={status}')
        except Exception as e:
            ok('Charge (decline)', False, str(e))
    else:
        ok('Charge (decline)', False, 'no decline_order_id')

    print_summary()


def print_summary():
    print('\n== Summary ==')
    print(f'Passed: {passed}, Failed: {failed}')


if __name__ == '__main__':
    main()
