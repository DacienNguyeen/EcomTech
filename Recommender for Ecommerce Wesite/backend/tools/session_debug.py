#!/usr/bin/env python3
"""
Session debug test
"""
import requests
from datetime import datetime

BASE = "http://127.0.0.1:8000"
s = requests.Session()

def main():
    print('\n== Session Debug ==')
    
    # Register and login
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    user = {
        "full_name": f"Session Test {ts}",
        "email": f"sessiontest_{ts}@example.com",
        "password": "testpass123"
    }
    
    # Register
    r = s.post(f"{BASE}/api/v1/users/register/", json=user)
    print(f"Register: {r.status_code}")
    print(f"Session after register: {s.cookies}")
    
    # Login
    r = s.post(f"{BASE}/api/v1/users/login/", json={"email": user['email'], "password": user['password']})
    print(f"Login: {r.status_code}")
    print(f"Session after login: {s.cookies}")
    
    # Test /me endpoint to see session
    r = s.get(f"{BASE}/api/v1/users/me/")
    print(f"Me endpoint: {r.status_code}")
    print(f"Me response: {r.text[:200]}")

if __name__ == '__main__':
    main()
