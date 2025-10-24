#!/usr/bin/env python3
"""
Debug script for API 500 errors
"""

import requests
import time
import subprocess
import sys

def test_external_api():
    """Test the external API directly"""
    print("🌐 Testing external API directly...")
    
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/EUR", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usd_rate = data.get("rates", {}).get("USD")
            print(f"✅ External API works: EUR/USD = {usd_rate}")
            return True
        else:
            print(f"❌ External API failed somehow: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ External API error: {e}")
        print(e)
        return False

def start_test_server():
    """Start the API server for testing"""
    print("🚀 Starting test server...")
    
    try:
        process = subprocess.Popen(
            ["uvicorn", "api_free:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "debug"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("   Waiting for server to start...")
        time.sleep(4)
        
        # Test if server is responding
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully")
                return process
            else:
                print(f"❌ Server not responding: {response.status_code}")
                stop_server_robust(process)
                return None
        except Exception as e:
            print(f"❌ Server connection failed: {e}")
            stop_server_robust(process)
            return None
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def stop_server_robust(process):
    """Robustly stop the API server using multiple methods"""
    if process is None:
        print("⚠️  No process to stop")
        return False

    stopped = False

    # Method 1: Gentle termination
    try:
        print("🔄 Attempting gentle termination...")
        process.terminate()
        process.wait(timeout=3)
        print("✅ Server stopped gracefully")
        stopped = True
    except subprocess.TimeoutExpired:
        print("⚠️  Gentle termination timed out, trying force kill...")
    except Exception as e:
        print(f"⚠️  Gentle termination failed: {e}")

    # Method 2: Force kill the process
    if not stopped:
        try:
            print("🔄 Force killing process...")
            process.kill()
            process.wait(timeout=3)
            print("✅ Server force killed")
            stopped = True
        except Exception as e:
            print(f"⚠️  Force kill failed: {e}")

    # Method 3: Kill by port (most robust)
    if not stopped:
        try:
            print("🔄 Killing by port 8000...")
            import subprocess as sp

            # Find process on port 8000
            result = sp.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.split('\n'):
                if ':8000' in line and ('LISTENING' in line or 'ABHÖREN' in line):
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        if pid.isdigit():
                            try:
                                sp.run(["taskkill", "/PID", pid, "/F"],
                                      capture_output=True, timeout=5)
                                print(f"✅ Killed process {pid} on port 8000")
                                stopped = True
                                break
                            except Exception:
                                pass
        except Exception as e:
            print(f"⚠️  Port-based kill failed: {e}")

    if not stopped:
        print("❌ Could not stop server - may need manual intervention")
        print("💡 Try: netstat -ano | findstr :8000")
        print("💡 Then: taskkill /PID <PID> /F")

    return stopped

def test_conversion(from_curr="EUR", to_curr="USD", amount="100"):
    """Test currency conversion"""
    print(f"💱 Testing conversion: {amount} {from_curr} -> {to_curr}")
    
    try:
        url = "http://127.0.0.1:8000/convert"
        params = {
            "from_currency": from_curr,
            "to_currency": to_curr,
            "amount": amount
        }
        
        print(f"   Request: {url}")
        print(f"   Params: {params}")
        
        response = requests.get(url, params=params, timeout=15)
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Conversion successful!")
            print(f"   Result: {data['amount']} {data['from']} = {data['result']} {data['to']}")
            print(f"   Rate: {data['info']['rate']}")
            print(f"   Cached: {data.get('cached', False)}")
            return True
        else:
            print(f"❌ Conversion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def check_logs():
    """Check the API logs"""
    print("📋 Checking API logs...")
    
    try:
        with open("api.log", "r") as f:
            content = f.read().strip()
            
        if content:
            print("📄 Log content:")
            print("-" * 40)
            print(content)
            print("-" * 40)
        else:
            print("📄 Log file is empty")
            
    except FileNotFoundError:
        print("📄 No log file found")
    except Exception as e:
        print(f"❌ Error reading logs: {e}")

def main():
    """Main debugging function"""
    print("🐛 API Error Debugging Tool")
    print("=" * 50)
    
    # Step 1: Test external API
    if not test_external_api():
        print("❌ External API is not working. Check internet connection.")
        return False
    
    print()
    
    # Step 2: Start local server
    process = start_test_server()
    if not process:
        print("❌ Could not start local server")
        return False
    
    try:
        print()
        
        # Step 3: Test basic conversion
        success = test_conversion("EUR", "USD", "100")
        
        print()
        
        # Step 4: Test different currencies
        if success:
            print("🧪 Testing other currency pairs...")
            test_conversion("USD", "EUR", "100")
            test_conversion("EUR", "GBP", "50")
            test_conversion("GBP", "JPY", "25")
        
        print()
        
        # Step 5: Test edge cases
        print("🧪 Testing edge cases...")
        test_conversion("EUR", "USD", "0.01")  # Small amount
        test_conversion("EUR", "USD", "99999999")  # Large amount
        test_conversion("EUR", "XYZ", "100")  # Invalid currency
        
        print()
        
        # Step 6: Check logs
        check_logs()
        
        return success
        
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        stop_server_robust(process)

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 API is working correctly!")
            print("💡 If you're still getting 500 errors in the GUI:")
            print("   1. Make sure you're using the Free API mode")
            print("   2. Check that the server starts properly")
            print("   3. Try restarting the GUI")
        else:
            print("\n❌ API has issues that need to be fixed")
        
    except KeyboardInterrupt:
        print("\n👋 Debugging interrupted")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        
    sys.exit(0 if success else 1)
