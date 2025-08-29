#!/usr/bin/env python3
"""Fast fail-fast cart test (JWT) with 6s timeout per request.

Behavior:
- BASE = http://127.0.0.1:8000/api/v1
- timeout default 6s for every request
- Step 1: GET /healthz/ -> must return 200
- Step 2: POST /users/login/ with email/password from env (USER_EMAIL/USER_PASS)
  - if 400 returned -> print hint to create user first and exit
  - on success extract token from response (token or access_token)
- Step 3: POST /orders/cart/items/ {book_id:1, qty:1} with Bearer token -> must return 200
- Step 4: GET /orders/cart/ -> must contain items length >= 1

Print format: [OK]/[FAIL] <status> <message>
On any failure exit with code 1.
"""
import os
import sys
import json

try:
    import requests
    from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError, HTTPError, Timeout
except ImportError:
    print("requests package not installed. Please run: pip install requests")
    sys.exit(1)


BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000/api/v1")
TIMEOUT = 6

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

def ok(msg):
    print(f"[OK] {msg}")

def do_request(method, path, **kwargs):
    url = BASE.rstrip('/') + path
    try:
        resp = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        return resp
    except ConnectTimeout:
        fail(f"ConnectTimeout when calling {url}")
    except ReadTimeout:
        fail(f"ReadTimeout when calling {url}")
    except Timeout:
        fail(f"Timeout when calling {url}")
    except ConnectionError as e:
        fail(f"ConnectionError when calling {url}: {e}")
    except Exception as e:
        fail(f"Request exception when calling {url}: {e}")


def step_health():
    resp = do_request('GET', '/healthz/')
    if resp.status_code == 200:
        ok(f"{resp.status_code} healthz OK")
    else:
        fail(f"{resp.status_code} healthz returned, body={resp.text}")


def step_login():
    email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASS')
    if not email or not password:
        fail('USER_EMAIL or USER_PASS env missing')

    payload = {'email': email, 'password': password}
    headers = {'Content-Type': 'application/json'}
    resp = do_request('POST', '/users/login/', json=payload, headers=headers)

    if resp.status_code == 200:
        try:
            data = resp.json()
        except Exception:
            fail(f'200 from login but invalid json: {resp.text}')
        token = data.get('access_token') or data.get('token') or data.get('data', {}).get('token')
        if not token:
            # sometimes token nested under key 'token' with user wrapper
            # try common shapes
            for v in data.values():
                if isinstance(v, str) and v.count('.') >= 2:
                    token = v
                    break
        if not token:
            fail('Login succeeded but no token found in response')
        ok(f"{resp.status_code} login OK, token len={len(token)}")
        return token
    elif resp.status_code == 400:
        # helpful hint
        fail(f"{resp.status_code} login failed - invalid credentials. Try creating the user first.")
    else:
        fail(f"{resp.status_code} login failed: {resp.text}")


def step_add_item(token):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'book_id': 1, 'qty': 1}
    resp = do_request('POST', '/orders/cart/items/', json=payload, headers=headers)
    if resp.status_code == 200:
        ok(f"{resp.status_code} add item OK")
    else:
        fail(f"{resp.status_code} add item failed: {resp.text}")


def step_get_cart(token):
    headers = {'Authorization': f'Bearer {token}'}
    resp = do_request('GET', '/orders/cart/', headers=headers)
    if resp.status_code != 200:
        fail(f"{resp.status_code} get cart failed: {resp.text}")
    try:
        data = resp.json()
    except Exception:
        fail(f"Invalid JSON from cart: {resp.text}")
    items = data.get('items')
    if not isinstance(items, list):
        fail(f"Cart items not a list: {items}")
    if len(items) >= 1:
        ok(f"{resp.status_code} cart has {len(items)} item(s)")
    else:
        fail(f"{resp.status_code} cart empty: {data}")


def main():
    print('Fast fail-fast cart test starting...')
    step_health()
    token = step_login()
    step_add_item(token)
    step_get_cart(token)
    print('\nAll steps passed')


if __name__ == '__main__':
    main()
