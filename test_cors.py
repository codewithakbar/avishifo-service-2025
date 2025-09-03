#!/usr/bin/env python3
"""
Simple CORS test script to verify the chat API endpoints
"""
import requests
import json

def test_cors_preflight():
    """Test CORS preflight request"""
    url = "https://new.avishifo.uz/api/chat/gpt/chats/632/send_message/"
    headers = {
        "Origin": "https://dashboard.avishifo.uz",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type, Authorization"
    }
    
    try:
        response = requests.options(url, headers=headers)
        print(f"OPTIONS request status: {response.status_code}")
        print(f"CORS headers in response:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing CORS preflight: {e}")
        return False

def test_cors_post():
    """Test CORS POST request"""
    url = "https://new.avishifo.uz/api/chat/gpt/chats/632/send_message/"
    headers = {
        "Origin": "https://dashboard.avishifo.uz",
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN_HERE"  # Replace with actual token
    }
    data = {
        "content": "Test message",
        "model": "gpt-4o"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"POST request status: {response.status_code}")
        print(f"CORS headers in response:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        return 'access-control-allow-origin' in response.headers
    except Exception as e:
        print(f"Error testing CORS POST: {e}")
        return False

if __name__ == "__main__":
    print("Testing CORS configuration...")
    print("=" * 50)
    
    print("\n1. Testing OPTIONS preflight request:")
    preflight_ok = test_cors_preflight()
    
    print("\n2. Testing POST request (requires valid token):")
    post_ok = test_cors_post()
    
    print("\n" + "=" * 50)
    print(f"Preflight test: {'PASS' if preflight_ok else 'FAIL'}")
    print(f"POST test: {'PASS' if post_ok else 'FAIL'}")
    
    if preflight_ok and post_ok:
        print("\n✅ CORS configuration appears to be working correctly!")
    else:
        print("\n❌ CORS configuration needs attention.")
