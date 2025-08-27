#!/usr/bin/env python3
"""Quick OpenAPI-driven smoke test for users endpoints.

Usage: python tools/swagger_api_test.py

This script fetches /api/schema/, lists the users-related paths, then
executes register -> login -> me -> logout -> me using a requests.Session
and prints concise results.
"""
import sys
import json
import requests

BASE = "http://127.0.0.1:8000"
SCHEMA_URL = f"{BASE}/api/schema/"


def fetch_schema():
    print("Fetching OpenAPI schema...", end=" ")
    r = requests.get(SCHEMA_URL, timeout=10)
    r.raise_for_status()
    print("OK")
    return r.json()


def pretty_resp(r):
    try:
        body = r.json()
        body = json.dumps(body, ensure_ascii=False)
    except Exception:
        body = r.text
    return f"{r.status_code} {r.reason}: {body}"


def run_users_flow():
    s = requests.Session()
    # sample user
    user = {
        "full_name": "Swagger Tester",
        "email": "swagger-tester@example.com",
        "phone": "0123456789",
        "address": "Test address",
        "password": "TestPass123!",
    }

    print('\n== Register ==')
    r = s.post(f"{BASE}/api/v1/users/register/", data=user, timeout=10)
    if r.status_code == 201:
        print('Registered:', pretty_resp(r))
    elif r.status_code == 400:
        print('Register returned 400 (maybe already exists):', pretty_resp(r))
    else:
        print('Register unexpected:', pretty_resp(r))

    print('\n== Login ==')
    login_data = {"email": user["email"], "password": user["password"]}
    r = s.post(f"{BASE}/api/v1/users/login/", data=login_data, timeout=10)
    print(pretty_resp(r))

    print('\n== Me (after login) ==')
    r = s.get(f"{BASE}/api/v1/users/me/", timeout=10)
    print(pretty_resp(r))

    print('\n== Logout ==')
    r = s.post(f"{BASE}/api/v1/users/logout/", timeout=10)
    print(pretty_resp(r))

    print('\n== Me (after logout) ==')
    r = s.get(f"{BASE}/api/v1/users/me/", timeout=10)
    print(pretty_resp(r))


def main():
    try:
        schema = fetch_schema()
    except Exception as e:
        print('Failed to fetch schema:', e)
        sys.exit(2)

    # print a tiny summary of users-related paths
    paths = [p for p in schema.get('paths', {}) if p.startswith('/api/v1/users')]
    print('\nUsers-related paths from schema:')
    for p in paths:
        print(' -', p)

    run_users_flow()


if __name__ == '__main__':
    main()
