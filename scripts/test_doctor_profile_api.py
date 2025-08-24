#!/usr/bin/env python3
"""
Test script for Doctor Profile API endpoints
This script tests all the new profile page endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your server URL
API_BASE = f"{BASE_URL}/api/doctors"

# Test data
TEST_PROFILE_DATA = {
    "full_name": "Доктор Ахмедов Алишер",
    "email": "alisher.ahmedov@example.com",
    "phone": "+998 90 123 45 67",
    "specialization": ["Кардиолог", "Эхокардиография"],
    "experience": "15 лет",
    "education": "Ташкентский медицинский университет",
    "bio": "Опытный кардиолог с 15-летним стажем работы. Специализируюсь на лечении сердечно-сосудистых заболеваний.",
    "languages": ["Узбекский", "Русский", "Английский"],
    "certifications": "Сертификат кардиолога, Европейское общество кардиологов",
    "date_of_birth": "1985-03-15",
    "gender": "Мужской",
    "address": "Улица Марифатчи, дом 15",
    "country": "Узбекистан",
    "region": "Хорезмская",
    "district": "Ургенчский",
    "emergency_contact": "+998 90 987 65 43",
    "medical_license": "MD-12345",
    "insurance": "Страховая компания 'Медицинская защита'",
    "working_hours": "9:00-18:00",
    "consultation_fee": "150,000 сум",
    "availability": "Понедельник - Пятница"
}

def print_separator(title):
    """Print a separator with title"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_endpoint(method, url, data=None, headers=None, expected_status=200):
    """Test an API endpoint and return the response"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print(f"❌ Unknown method: {method}")
            return None
        
        print(f"✅ {method.upper()} {url}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   ✅ Expected status {expected_status}")
        else:
            print(f"   ❌ Expected status {expected_status}, got {response.status_code}")
        
        if response.content:
            try:
                response_data = response.json()
                print(f"   Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"   Response: {response.text}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_profile_page_endpoints():
    """Test the profile page endpoints"""
    print_separator("Testing Profile Page Endpoints")
    
    # Note: These endpoints require authentication
    # In a real test, you would need to get a valid JWT token first
    
    print("🔒 Note: These endpoints require authentication (JWT token)")
    print("   To test properly, you need to:")
    print("   1. Login as a doctor user")
    print("   2. Get the JWT token")
    print("   3. Include it in the Authorization header")
    
    # Test endpoints without authentication (will return 401)
    headers = {"Content-Type": "application/json"}
    
    # Test GET /profile/page/
    print("\n--- Testing GET /profile/page/ ---")
    test_endpoint("GET", f"{API_BASE}/profile/page/", headers=headers, expected_status=401)
    
    # Test PATCH /profile/page/
    print("\n--- Testing PATCH /profile/page/ ---")
    test_endpoint("PATCH", f"{API_BASE}/profile/page/", data=TEST_PROFILE_DATA, headers=headers, expected_status=401)
    
    # Test GET /profile/stats/
    print("\n--- Testing GET /profile/stats/ ---")
    test_endpoint("GET", f"{API_BASE}/profile/stats/", headers=headers, expected_status=401)
    
    # Test GET /profile/fields-info/
    print("\n--- Testing GET /profile/fields-info/ ---")
    test_endpoint("GET", f"{API_BASE}/profile/fields-info/", headers=headers, expected_status=401)
    
    # Test GET /profile/options/
    print("\n--- Testing GET /profile/options/ ---")
    test_endpoint("GET", f"{API_BASE}/profile/options/", headers=headers, expected_status=401)

def test_public_endpoints():
    """Test endpoints that don't require authentication"""
    print_separator("Testing Public Endpoints")
    
    # Test GET /specialties/
    print("\n--- Testing GET /specialties/ ---")
    test_endpoint("GET", f"{API_BASE}/specialties/", expected_status=200)
    
    # Test GET /specialties/stats/
    print("\n--- Testing GET /specialties/stats/ ---")
    test_endpoint("GET", f"{API_BASE}/specialties/stats/", expected_status=200)
    
    # Test GET /specialties/choices/
    print("\n--- Testing GET /specialties/choices/ ---")
    test_endpoint("GET", f"{API_BASE}/specialties/choices/", expected_status=200)

def test_with_authentication():
    """Test endpoints with authentication (requires valid token)"""
    print_separator("Testing with Authentication")
    
    print("🔑 To test with authentication, you need to:")
    print("   1. Create a doctor user account")
    print("   2. Login to get JWT token")
    print("   3. Use the token in requests")
    
    print("\nExample with token:")
    print("""
    # Get token from login
    login_response = requests.post(f"{BASE_URL}/api/accounts/login/", {
        "username": "doctor_username",
        "password": "doctor_password"
    })
    token = login_response.json()["access"]
    
    # Use token in requests
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test authenticated endpoints
    response = requests.get(f"{API_BASE}/profile/page/", headers=headers)
    print(response.json())
    """)

def main():
    """Main test function"""
    print("🚀 Doctor Profile API Test Script")
    print(f"Testing against: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    
    try:
        # Test public endpoints first
        test_public_endpoints()
        
        # Test profile page endpoints (without auth)
        test_profile_page_endpoints()
        
        # Show authentication instructions
        test_with_authentication()
        
        print_separator("Test Summary")
        print("✅ Public endpoints tested")
        print("🔒 Profile endpoints require authentication")
        print("📚 Check the API documentation for proper usage")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
