#!/usr/bin/env python3
"""
Quick test to verify registration works without hanging
"""

import requests
import sys
import time

API_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Registration Endpoint")
print("=" * 60)
print()

# Test data
test_user = {
    "full_name": "Test User",
    "email": f"test{int(time.time())}@example.com",  # Unique email
    "password": "Test123!@#"
}

print(f"Attempting to register user: {test_user['email']}")
print("Sending POST request...")

try:
    start_time = time.time()

    response = requests.post(
        f"{API_URL}/api/auth/register",
        json=test_user,
        timeout=5  # 5 second timeout
    )

    elapsed = time.time() - start_time

    print(f"Response received in {elapsed:.2f} seconds")
    print(f"Status Code: {response.status_code}")
    print()

    if response.status_code == 200:
        print("✓ SUCCESS - Registration completed!")
        data = response.json()
        print(f"User ID: {data['user']['id']}")
        print(f"Email: {data['user']['email']}")
        print(f"Email Verified: {data['user'].get('email_verified', False)}")
        print()
        print("Note: Email verification not sent (SMTP not configured)")
        print("This is expected in development mode.")
    elif response.status_code == 400:
        print("✗ FAILED - Bad Request")
        print(f"Error: {response.json()}")
    else:
        print(f"✗ FAILED - Unexpected status code")
        print(f"Response: {response.text}")

except requests.exceptions.Timeout:
    print("✗ FAILED - Request timed out after 5 seconds")
    print()
    print("This means the backend is still hanging.")
    print("Make sure you:")
    print("  1. Stopped the old backend server (Ctrl+C)")
    print("  2. Started it again (to load new .env)")
    sys.exit(1)

except requests.exceptions.ConnectionError:
    print("✗ FAILED - Cannot connect to backend")
    print()
    print("Make sure the backend server is running:")
    print("  cd backend")
    print("  start-server.bat")
    sys.exit(1)

except Exception as e:
    print(f"✗ FAILED - Unexpected error: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("Test Complete")
print("=" * 60)
