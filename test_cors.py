#!/usr/bin/env python3
"""
Simple CORS test script to verify the Django backend is properly configured
"""

import requests
import json

def test_cors():
    """Test CORS configuration for various endpoints"""
    
    base_url = "https://new.avishifo.uz"
    test_endpoints = [
        "/api/cors-test/",
        "/api/chat/health/",
        "/api/chat/gpt/chats/1/send_message/",  # This is the problematic endpoint
    ]
    
    headers = {
        "Origin": "https://dashboard.avishifo.uz",
        "Content-Type": "application/json",
    }
    
    print("Testing CORS configuration...")
    print("=" * 50)
    
    for endpoint in test_endpoints:
        url = base_url + endpoint
        print(f"\nTesting: {url}")
        
        try:
            # Test OPTIONS request (preflight)
            print("  Testing OPTIONS request...")
            options_response = requests.options(url, headers=headers)
            print(f"    Status: {options_response.status_code}")
            print(f"    CORS Headers:")
            for header, value in options_response.headers.items():
                if 'access-control' in header.lower():
                    print(f"      {header}: {value}")
            
            # Test POST request (if it's a POST endpoint)
            if 'send_message' in endpoint:
                print("  Testing POST request...")
                post_data = {"content": "Test message"}
                post_response = requests.post(url, headers=headers, json=post_data)
                print(f"    Status: {post_response.status_code}")
                print(f"    CORS Headers:")
                for header, value in post_response.headers.items():
                    if 'access-control' in header.lower():
                        print(f"      {header}: {value}")
            
        except Exception as e:
            print(f"    Error: {e}")
    
    print("\n" + "=" * 50)
    print("CORS test completed!")

if __name__ == "__main__":
    test_cors()
