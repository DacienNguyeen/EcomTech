#!/usr/bin/env python3

import os
import sys
import django
import requests
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

def test_activity_api():
    url = 'http://127.0.0.1:8000/api/v1/activities/'
    
    # Test data
    data = {
        'book_id': 1,
        'action': 'test_view',
        'activity_time': datetime.now().isoformat()
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"Testing activity API at {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"\nResponse status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Activity tracking API working!")
        else:
            print("❌ Activity tracking API error")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    test_activity_api()
