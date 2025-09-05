#!/usr/bin/env python3

import os
import sys
import django
import time
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from apps.activities.models import UserActivity

def monitor_activities():
    print("🔍 Monitoring user activities in real-time...")
    print("Open frontend at http://localhost:3000 and interact with products")
    print("Press Ctrl+C to stop monitoring\n")
    
    last_count = UserActivity.objects.count()
    print(f"Initial activity count: {last_count}\n")
    
    try:
        while True:
            current_count = UserActivity.objects.count()
            
            if current_count > last_count:
                # New activities detected
                new_activities = UserActivity.objects.all().order_by('-ActivityTime')[:current_count - last_count]
                
                print(f"📊 {current_count - last_count} new activities detected:")
                for activity in reversed(new_activities):
                    timestamp = activity.ActivityTime.strftime('%H:%M:%S')
                    print(f"  [{timestamp}] CustomerID:{activity.CustomerID} → BookID:{activity.BookID} → Action:{activity.Action}")
                
                print(f"Total activities: {current_count}\n")
                last_count = current_count
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n👋 Stopping activity monitor...")
        print(f"Final activity count: {UserActivity.objects.count()}")

if __name__ == '__main__':
    monitor_activities()
