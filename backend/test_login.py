import requests
import json

# Test the login endpoint
url = "http://localhost:8000/api/auth/login"
data = {
    "email": "driver@test.com",
    "password": "password123"
}

print(f"Testing login at: {url}")
print(f"Data: {data}")
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    print()
    
    if response.status_code == 200:
        print(f"Success! Token: {response.json()}")
    else:
        print(f"Error Response: {response.text}")
        
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: Cannot connect to {url}")
    print("Make sure the backend is running on port 8000")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
