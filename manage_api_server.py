#!/usr/bin/env python3
"""
API Server Management Utility
Manually start/stop/check the API server
"""

import subprocess
import time

def check_server_status():
    """Check if API server is running on port 8000"""
    print("🔍 Checking server status...")

    # Method 1: Check if our API is responding correctly
    try:
        import requests

        # Test root endpoint
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"📡 Server response on /: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                if "message" in data and "Calculator" in str(data):
                    print("✅ Our API Server is running correctly on port 8000")
                    pid = get_pid_on_port(8000)
                    if pid:
                        print(f"   Process ID: {pid}")
                    return pid if pid else "responding"
                else:
                    print("⚠️  Different server running on port 8000")
                    print(f"   Response: {data}")
            except Exception:
                print("⚠️  Server on port 8000 is not our API (non-JSON response)")

        # Test API endpoint specifically
        print("🧪 Testing API conversion endpoint...")
        api_response = requests.get(
            "http://127.0.0.1:8000/convert",
            params={"from_currency": "EUR", "to_currency": "USD", "amount": "1"},
            timeout=5
        )

        if api_response.status_code == 200:
            print("✅ API conversion endpoint is working!")
            data = api_response.json()
            print(f"   Test conversion: 1 EUR = {data.get('result', 'N/A')} USD")
            pid = get_pid_on_port(8000)
            return pid if pid else "responding"
        else:
            print(f"❌ API conversion endpoint failed: {api_response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ No server responding on port 8000")
    except Exception as e:
        print(f"⚠️  API test failed: {e}")

    # Method 2: Check port usage with netstat
    pid = get_pid_on_port(8000)
    if pid:
        print(f"⚠️  Process found on port 8000 (PID: {pid}) but it's not our API server")
        print("💡 This might be a different application using port 8000")
        print("💡 Try stopping it first, then start our API server")
        return pid
    else:
        print("❌ No process found on port 8000")
        return None

def get_pid_on_port(port, debug=False):
    """Get PID of process using specified port"""
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if debug:
            print(f"🔍 Looking for port {port} in netstat output...")

        for line in result.stdout.split('\n'):
            if f':{port}' in line:
                if debug:
                    print(f"   Found line: {line}")

                # Check for various forms of LISTENING status
                listening_indicators = ['LISTENING', 'ABHÖREN', 'LISTEN', 'ABH?REN', 'ABHOREN', 'ABH™REN']
                if any(indicator in line for indicator in listening_indicators):
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        if pid.isdigit():
                            if debug:
                                print(f"   Extracted PID: {pid}")
                            return pid
                elif debug:
                    print("   Line doesn't contain listening indicators")

        if debug:
            print(f"   No listening process found on port {port}")
        return None

    except Exception as e:
        print(f"❌ Error checking port {port}: {e}")
        return None

def stop_server():
    """Stop the API server"""
    print("🛑 Stopping API server...")

    # Get PID directly with debug info
    pid = get_pid_on_port(8000, debug=True)
    if not pid:
        print("ℹ️  No server found on port 8000")
        return True

    print(f"📋 Found server process (PID: {pid})")

    try:
        print("🔄 Attempting to stop server...")
        result = subprocess.run(["taskkill", "/PID", pid, "/F"],
                               capture_output=True, timeout=5, text=True)

        if result.returncode == 0:
            print(f"✅ Successfully sent kill signal to PID {pid}")
        else:
            print(f"⚠️  Kill command returned code {result.returncode}")
            print(f"   Output: {result.stdout}")
            print(f"   Error: {result.stderr}")

        # Wait a moment for process to terminate
        time.sleep(2)

        # Check if process is still running
        new_pid = get_pid_on_port(8000)
        if not new_pid:
            print("✅ Server stopped successfully!")

            # Double-check by testing API
            try:
                import requests
                requests.get("http://127.0.0.1:8000/convert", timeout=2)
                print("⚠️  API still responding - server may have restarted")
                return False
            except requests.exceptions.ConnectionError:
                print("✅ Confirmed: API server is no longer responding")
                return True
            except Exception:
                print("✅ Server appears to be stopped")
                return True
        else:
            if new_pid == pid:
                print(f"❌ Server is still running (same PID: {pid})")
            else:
                print(f"⚠️  Different server now running (new PID: {new_pid})")
            return False

    except Exception as e:
        print(f"❌ Failed to stop server: {e}")
        return False

def start_free_server():
    """Start the free API server"""
    print("🚀 Starting Free API server...")
    
    # Check if already running
    if check_server_status():
        print("ℹ️  Server is already running")
        return False
    
    try:
        print("   Command: uvicorn corally.api.free_server:app --host 127.0.0.1 --port 8000")
        subprocess.Popen(
            ["uvicorn", "corally.api.free_server:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        if check_server_status():
            print("✅ Free API server started successfully!")
            print("🌐 Test it: http://127.0.0.1:8000")
            print("💱 Convert: http://127.0.0.1:8000/convert?from_currency=EUR&to_currency=USD&amount=100")
            return True
        else:
            print("❌ Server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def start_paid_server():
    """Start the paid API server (requires .env file)"""
    print("🚀 Starting Paid API server...")
    
    # Check if already running
    if check_server_status():
        print("ℹ️  Server is already running")
        return False
    
    # Check for .env file
    import os
    if not os.path.exists(".env"):
        print("❌ .env file not found. Create it with: API_KEY=your_key")
        return False
    
    try:
        print("   Command: uvicorn corally.api.server:app --host 127.0.0.1 --port 8000 --reload")
        subprocess.Popen(
            ["uvicorn", "corally.api.server:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(5)
        
        if check_server_status():
            print("✅ Paid API server started successfully!")
            print("🌐 Test it: http://127.0.0.1:8000")
            return True
        else:
            print("❌ Server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def test_server():
    """Test if the server is responding"""
    print("🧪 Testing API server...")

    try:
        import requests

        # Test conversion endpoint directly (this is what matters)
        print("💱 Testing currency conversion...")
        conv_response = requests.get(
            "http://127.0.0.1:8000/convert",
            params={"from_currency": "EUR", "to_currency": "USD", "amount": "100"},
            timeout=10
        )

        if conv_response.status_code == 200:
            data = conv_response.json()
            print("✅ Conversion test successful!")
            print(f"   {data['amount']} {data['from']} = {data['result']} {data['to']}")
            print(f"   Rate: {data['info']['rate']}")
            print(f"   Cached: {data.get('cached', False)}")

            # Test different currency pair
            print("\n💱 Testing different currency pair...")
            conv_response2 = requests.get(
                "http://127.0.0.1:8000/convert",
                params={"from_currency": "GBP", "to_currency": "JPY", "amount": "50"},
                timeout=10
            )

            if conv_response2.status_code == 200:
                data2 = conv_response2.json()
                print("✅ Second conversion test successful!")
                print(f"   {data2['amount']} {data2['from']} = {data2['result']} {data2['to']}")
                print(f"   Rate: {data2['info']['rate']}")
                print(f"   Cached: {data2.get('cached', False)}")

                print("\n🎉 API server is working perfectly!")
                return True
            else:
                print(f"⚠️  Second conversion failed: {conv_response2.status_code}")
                print("✅ But basic conversion works, so server is functional")
                return True
        else:
            print(f"❌ Conversion test failed: {conv_response.status_code}")
            print(f"   Response: {conv_response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on port 8000")
        print("💡 Make sure the API server is running")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main menu"""
    print("🔧 API Server Management Utility")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Check server status")
        print("2. Start Free API server")
        print("3. Start Paid API server")
        print("4. Stop server")
        print("5. Test server")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                check_server_status()
            elif choice == "2":
                start_free_server()
            elif choice == "3":
                start_paid_server()
            elif choice == "4":
                stop_server()
            elif choice == "5":
                test_server()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
