#!/usr/bin/env python3

import os
import sys
import django
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from apps.activities.models import UserActivity

def test_activity_api():
    print("Testing activity API with Django test client...")
    
    # Create test client
    client = Client()
    
    # Test data
    data = {
        'book_id': 1,
        'action': 'view',
        'activity_time': datetime.now().isoformat()
    }
    
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    # Get initial count
    initial_count = UserActivity.objects.count()
    print(f"Initial activity count: {initial_count}")
    
    try:
        # Test POST request
        response = client.post(
            '/api/v1/activities/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        # Check if new activity was created
        final_count = UserActivity.objects.count()
        print(f"Final activity count: {final_count}")
        
        if response.status_code == 401:
            print("⚠️  Authentication required (expected for IsAuthenticated permission)")
        elif response.status_code == 201:
            print("✅ Activity tracking API working!")
        else:
            print("❌ Activity tracking API error")
            
        # Show recent activities
        print("\nRecent activities:")
        activities = UserActivity.objects.all().order_by('-ActivityTime')[:3]
        for activity in activities:
            print(f'  - CustomerID: {activity.CustomerID}, BookID: {activity.BookID}, Action: {activity.Action}')
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    test_activity_api()
