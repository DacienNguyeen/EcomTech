#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

def test_frontend_integration():
    base_url = 'http://127.0.0.1:8000/api/v1'
    
    print("🚀 Testing frontend-backend integration...")
    print("Simulating user interactions with activity tracking\n")
    
    # Test scenarios
    test_cases = [
        {'book_id': 1, 'action': 'view', 'description': 'User views Book 1'},
        {'book_id': 2, 'action': 'view', 'description': 'User views Book 2'}, 
        {'book_id': 1, 'action': 'add_to_cart', 'description': 'User adds Book 1 to cart'},
        {'book_id': 3, 'action': 'view', 'description': 'User views Book 3'},
        {'book_id': 2, 'action': 'add_to_cart', 'description': 'User adds Book 2 to cart'},
    ]
    
    headers = {'Content-Type': 'application/json'}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📊 Test {i}: {test_case['description']}")
        
        payload = {
            'book_id': test_case['book_id'],
            'action': test_case['action'],
            'activity_time': datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                f"{base_url}/activities/",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ Success - Activity ID: {result.get('id')}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Cannot connect to backend server")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
        
        # Wait between requests to see real-time monitoring
        time.sleep(3)
    
    print("\n🎯 Testing recommendation engine with new activity data...")
    try:
        response = requests.get(f"{base_url}/recommendations/v1/content/?k=4")
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('results', [])
            print(f"✅ Recommendation API working - Found {len(recommendations)} recommendations")
            if recommendations:
                print("   Sample recommendation:")
                rec = recommendations[0]
                print(f"   - BookID: {rec.get('BookID')}, Title: {rec.get('title')}")
        else:
            print(f"❌ Recommendation API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Recommendation API error: {e}")
    
    print("\n✨ Integration test completed!")

if __name__ == '__main__':
    test_frontend_integration()
