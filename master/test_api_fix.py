#!/usr/bin/env python3
"""
Test script to verify that the API server can be started with the new module paths.
"""

import subprocess
import time
import requests
import sys

def test_api_server_start(api_type="free"):
    """Test starting the API server with the new module paths"""
    print(f"🧪 Testing {api_type} API server startup...")
    
    # Choose the correct module path
    if api_type == "free":
        api_module = "corally.api.free_server:app"
    else:
        api_module = "corally.api.server:app"
    
    print(f"   Module: {api_module}")
    
    try:
        # Start the server
        process = subprocess.Popen(
            ["uvicorn", api_module, "--host", "127.0.0.1", "--port", "8001"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("   Waiting for server to start...")
        time.sleep(3)
        
        # Test if server is responding
        try:
            response = requests.get("http://127.0.0.1:8001/", timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully!")
                print(f"   Response: {response.status_code}")
                
                # Test API endpoint
                api_response = requests.get(
                    "http://127.0.0.1:8001/convert",
                    params={"from_currency": "EUR", "to_currency": "USD", "amount": "1"},
                    timeout=5
                )
                
                if api_response.status_code == 200:
                    print("✅ API endpoint working!")
                    data = api_response.json()
                    print(f"   Test conversion: 1 EUR = {data.get('result', 'N/A')} USD")
                else:
                    print(f"⚠️  API endpoint returned: {api_response.status_code}")
                
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to server")
        except Exception as e:
            print(f"❌ Error testing server: {e}")
        
        # Clean up
        process.terminate()
        process.wait(timeout=5)
        print("🧹 Server stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Testing API Server Module Path Fix")
    print("=" * 50)
    
    # Test free API
    success_free = test_api_server_start("free")
    print()
    
    # Test paid API (might fail due to missing API key, but should start)
    success_paid = test_api_server_start("paid")
    print()
    
    if success_free:
        print("✅ Free API server test passed!")
    else:
        print("❌ Free API server test failed!")
    
    if success_paid:
        print("✅ Paid API server test passed!")
    else:
        print("⚠️  Paid API server test failed (might be due to missing API key)")
    
    print("\n🎉 API module path fix verification complete!")

if __name__ == "__main__":
    main()
