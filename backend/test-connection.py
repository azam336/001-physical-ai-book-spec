#!/usr/bin/env python3
"""
Quick test script to verify backend API is accessible
"""

import requests
import sys

API_URL = "http://localhost:8000"

print("=" * 60)
print("Testing Backend API Connection")
print("=" * 60)
print()

# Test 1: Health check
print("Test 1: Health Check Endpoint")
print(f"GET {API_URL}/api/health")
try:
    response = requests.get(f"{API_URL}/api/health", timeout=5)
    if response.status_code == 200:
        print("✓ SUCCESS - Backend is running!")
        print(f"  Response: {response.json()}")
    else:
        print(f"✗ FAILED - Status: {response.status_code}")
        print(f"  Response: {response.text}")
except requests.exceptions.ConnectionError:
    print("✗ FAILED - Cannot connect to backend")
    print("  Error: Connection refused")
    print()
    print("SOLUTION: Start the backend server with:")
    print("  cd backend")
    print("  .venv\\Scripts\\activate")
    print("  uvicorn app.main:app --reload")
    print()
    print("  OR double-click: backend/start-server.bat")
    sys.exit(1)
except Exception as e:
    print(f"✗ FAILED - Error: {e}")
    sys.exit(1)

print()

# Test 2: CORS headers
print("Test 2: CORS Configuration")
print(f"OPTIONS {API_URL}/api/health")
try:
    response = requests.options(
        f"{API_URL}/api/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        },
        timeout=5
    )

    cors_origin = response.headers.get("Access-Control-Allow-Origin")
    cors_methods = response.headers.get("Access-Control-Allow-Methods")

    if cors_origin == "http://localhost:3000":
        print("✓ SUCCESS - CORS configured correctly")
        print(f"  Allow-Origin: {cors_origin}")
        print(f"  Allow-Methods: {cors_methods}")
    else:
        print(f"✗ WARNING - CORS may have issues")
        print(f"  Allow-Origin: {cors_origin}")
except Exception as e:
    print(f"✗ FAILED - Error: {e}")

print()

# Test 3: Auth endpoints exist
print("Test 3: Auth Endpoints")
endpoints = [
    "/api/auth/register",
    "/api/auth/login",
    "/api/auth/logout"
]

for endpoint in endpoints:
    url = f"{API_URL}{endpoint}"
    try:
        # POST without credentials (should fail with 400 or 422, not 404)
        response = requests.post(url, json={}, timeout=5)
        if response.status_code in [400, 422, 401]:
            print(f"✓ {endpoint} - EXISTS")
        elif response.status_code == 404:
            print(f"✗ {endpoint} - NOT FOUND")
        else:
            print(f"? {endpoint} - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ {endpoint} - Error: {e}")

print()
print("=" * 60)
print("Backend API Test Complete")
print("=" * 60)
print()
print("If all tests passed, your frontend should work!")
print("If tests failed, check the error messages above.")
