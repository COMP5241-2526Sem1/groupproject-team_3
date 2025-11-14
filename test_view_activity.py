"""
Test the view_activity route with actual data
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from flask import session
from bson import ObjectId

app = create_app('development')

with app.test_client() as client:
    # First login as student
    print("1. Logging in as student...")
    response = client.post('/auth/login', data={
        'username': 'student_demo',
        'password': 'Demo@2024'
    }, follow_redirects=True)
    
    print(f"   Login status: {response.status_code}")
    
    # Now try to view the activity
    activity_id = "6916d2131476b67917e4c381"
    print(f"\n2. Viewing activity {activity_id}...")
    
    response = client.get(f'/student/activity/{activity_id}')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ SUCCESS! Page loaded without errors")
        
        # Check if AI evaluation is in the response
        if b'AI Evaluation' in response.data:
            print("   ✅ AI Evaluation section found!")
        else:
            print("   ⚠️ AI Evaluation section not found in HTML")
            
        # Check for error messages
        if b'Error' in response.data and b'Undefined' in response.data:
            print("   ❌ ERROR: Still contains 'Undefined' error message")
        else:
            print("   ✅ No 'Undefined' error in response")
    else:
        print(f"   ❌ FAILED with status {response.status_code}")
        print(f"   Response preview: {response.data[:500]}")
