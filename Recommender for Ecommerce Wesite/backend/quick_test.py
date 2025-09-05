import requests
import json

def test_api():
    print("Testing Recommendation API...")
    
    try:
        # Test basic connection
        print("1. Testing basic connection...")
        response = requests.get("http://localhost:8000/api/v1/recommendations/test/")
        print(f"Basic test: {response.status_code}")
        
        # Test content recommendations
        print("\n2. Testing content recommendations...")
        response = requests.get("http://localhost:8000/api/v1/recommendations/v1/content/?k=5")
        print(f"Content API status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Got {len(data.get('recommendations', []))} recommendations")
            for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
                print(f"  {i}. {rec.get('title', 'N/A')} - Score: {rec.get('score', 0)}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()
