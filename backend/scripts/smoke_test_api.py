import requests

BASE = 'http://localhost:8000/api'

print('Checking backend at', BASE)

# Register a user (use random email to avoid conflict)
email = 'smoketest_user@example.com'
password = 'TestPass123!'

reg_payload = {
    'first_name': 'Smoke',
    'last_name': 'Test',
    'email': email,
    'password': password,
    'phone': '+10000000000',
    'role': 'driver'
}

try:
    r = requests.post(f'{BASE}/auth/register', json=reg_payload, timeout=5)
    print('Register status:', r.status_code, r.text)
except Exception as e:
    print('Register error:', e)

# Login
try:
    r = requests.post(f'{BASE}/auth/login', json={'email': email, 'password': password}, timeout=5)
    print('Login status:', r.status_code, r.text)
    if r.status_code == 200:
        token = r.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        r2 = requests.get(f'{BASE}/auth/me', headers=headers, timeout=5)
        print('/me status:', r2.status_code, r2.text)
except Exception as e:
    print('Login or /me error:', e)
