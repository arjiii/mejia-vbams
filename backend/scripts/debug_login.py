"""
Debug script to test the complete login flow
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("VBAMS Login Flow Debug")
print("=" * 60)

# Step 1: Check if backend is running
print("\n1. Checking backend health...")
try:
    health = requests.get(f"{BASE_URL}/health")
    print(f"   ✓ Backend is running: {health.json()}")
except Exception as e:
    print(f"   ✗ Backend not accessible: {e}")
    exit(1)

# Step 2: Check if the auth endpoint exists
print("\n2. Checking API docs...")
try:
    docs = requests.get(f"{BASE_URL}/docs")
    print(f"   ✓ API docs accessible (Status: {docs.status_code})")
except Exception as e:
    print(f"   ✗ API docs not accessible: {e}")

# Step 3: Test login with exact data
print("\n3. Testing login endpoint...")
login_url = f"{BASE_URL}/api/auth/login"
print(f"   URL: {login_url}")

login_data = {
    "email": "driver@test.com",
    "password": "password123"
}
print(f"   Data: {json.dumps(login_data, indent=2)}")

try:
    response = requests.post(
        login_url,
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n   Status Code: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    print(f"   Response: {response.text[:500]}")  # First 500 chars
    
    if response.status_code == 200:
        print("\n   ✓ LOGIN SUCCESSFUL!")
        token_data = response.json()
        print(f"   Token: {token_data.get('access_token', 'N/A')[:50]}...")
    else:
        print(f"\n   ✗ LOGIN FAILED")
        print(f"   Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print(f"   ✗ Cannot connect to {login_url}")
    print("   Make sure backend is running on port 8000")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Check what frontend would send
print("\n4. Frontend API call simulation...")
print("   Frontend would call: POST /api/auth/login")
print("   With headers: {'Content-Type': 'application/json'}")
print(f"   And body: {json.dumps(login_data)}")

print("\n" + "=" * 60)
