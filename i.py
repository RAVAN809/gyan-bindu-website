import jwt
import json
import requests
from datetime import datetime

def analyze_token(token):
    """JWT token ko analyze karen"""
    
    print("🔐 JWT TOKEN ANALYSIS")
    print("=" * 50)
    
    try:
        # Token decode karen (without verification)
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        print("✅ Token Successfully Decoded!")
        print(f"📅 Issued At: {datetime.fromtimestamp(decoded['iat'])}")
        
        print("\n📋 PAYLOAD DATA:")
        payload = decoded.get('con', {})
        for key, value in payload.items():
            print(f"   {key}: {value}")
            
        # Special observations
        print(f"\n🎯 KEY OBSERVATIONS:")
        print(f"   - device_type: {payload.get('device_type', 'NOT FOUND')}")
        print(f"   - device_version: {payload.get('device_version', 'NOT FOUND')}")
        print(f"   - app_type: {'WEB' if 'Mozilla' in payload.get('device_version', '') else 'MOBILE'}")
        
        return payload
        
    except Exception as e:
        print(f"❌ Token decode error: {e}")
        return None

def test_with_token(token):
    """Is token ke saath API test karen"""
    
    print("\n🔧 TESTING WITH USER TOKEN")
    print("=" * 50)
    
    headers = {
        "Host": "elearn.crwilladmin.com",
        "appver": "101", 
        "apptype": "android",
        "cwkey": "+HwN3zs4tPU0p8BpOG5ZlXIU6MaWQmnMHXMJLLFcJ5m4kWqLXGLpsp8+2ydtILXy",
        "content-type": "application/json; charset=UTF-8",
        "user-agent": "okhttp/5.0.0-alpha.2",
        "token": token,
        "usertype": "2"
    }
    
    test_urls = [
        "https://elearn.crwilladmin.com/api/v8/batch-topic/3302?type=class",
        "https://elearn.crwilladmin.com/api/v8/my-batch",
        "https://elearn.crwilladmin.com/api/v9/batch-topic/3302?type=class"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url.split('/')[-1]}")
        
        try:
            response = requests.get(url, headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ SUCCESS! Data keys: {list(data.keys())}")
                if 'data' in data:
                    print(f"   📊 Data structure: {list(data['data'].keys())}")
            else:
                print(f"   ❌ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   💥 Exception: {e}")

# Your actual token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NjA3MzE3MjQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiIiLCJpZCI6ImEzTjFXWGMwZURKNWQyeExiWFJ0VkVaRldqaG9VVDA5IiwiZmlyc3RfbmFtZSI6IlZUQlZSMVpxVURBMVNqY3hXVVZDUTBORFEyb3ZVVDA5IiwiZW1haWwiOiJZbVFyTWtaelFXZ3lNWEV5WTFVclVFWXhSWGhRV21oRE4xaFNVSEk1VUdOYU1VczNiamt4U0hWcFp6MD0iLCJwaG9uZSI6IlptSmlZVVZVZW1ONWMxcE5NR3hyTVdOSGJWRmhRVDA5IiwiYXZhdGFyIjoiIiwicmVmZXJyYWxfY29kZSI6ImMwOURSRE54ZURKNWQyeExiWFJ0VkVaRldqaG9VVDA5IiwiZGV2aWNlX3R5cGUiOiJ3ZWIiLCJkZXZpY2VfdmVyc2lvbiI6Ik1vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTdfMl8xIGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNS41IFNhZmFyaS82MDQuMSIsImRldmljZV9tb2RlbCI6Ik1vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTdfMl8xIGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNS41IFNhZmFyaS82MDQuMSIsInJlbW90ZV9hZGRyIjoiNDQuMjIxLjYwLjI0In19.fl3LHRrazy4Z5vN5g2KuLSag0fa1i4Az-8DqAfcwRmJhKhLyc9ceHZ7oor5HcuzjDQr931Qrn9PkQ0J5tGwe2Qrm28ve3b9nNBcCfobbBl_8zTsSpFc0kNtGxKRZbUl9R_mAi23HGLhOdfrztVzstOzBMyLaXDvUWAPfl3OtDoV6bL92CEil_haHfoF1wHiwVG6bUgPiQ6UbTSPuSSoF8XtOHxADDJcekSFVEFSFfy_qwYgc4q5kvNrnKE-QLVed0DVHcuQlomtqUMcJ1qBP7a3AvIF7Hi95soCVJsMIQQGCmFRG5wR8TNxIdqRDt9fHR1Yb_K2MwZiIUj5HF35kQg"

# Analyze token
payload = analyze_token(token)

# Test with token
test_with_token(token)
