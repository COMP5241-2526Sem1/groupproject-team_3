"""
Test local server endpoint
"""
import requests

activity_id = "6916d2131476b67917e4c381"
url = f"http://localhost:5000/student/activity/{activity_id}"

try:
    # Need to be logged in first
    session = requests.Session()
    
    # Login
    login_url = "http://localhost:5000/auth/login"
    login_data = {
        "username": "student_demo",
        "password": "Demo@2024"  # Adjust if needed
    }
    
    print(f"Attempting login...")
    response = session.post(login_url, data=login_data, allow_redirects=False)
    print(f"Login status: {response.status_code}")
    
    # Now try to access the activity
    print(f"\nAccessing activity: {url}")
    response = session.get(url)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Page loaded successfully!")
        # Check if AI evaluation is in the response
        if 'AI Evaluation' in response.text:
            print("✅ AI Evaluation section found in page!")
        else:
            print("⚠️ AI Evaluation section NOT found")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
