#!/usr/bin/env python3
"""
Fix script to clear port 8000 and test API
"""

import subprocess
import time
import requests

def kill_processes_on_port(port=8000):
    """Kill any processes using the specified port"""
    print(f"🔍 Checking for processes on port {port}...")
    
    try:
        # Get processes using the port
        result = subprocess.run(
            ["netstat", "-ano"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        pids_to_kill = []
        for line in result.stdout.split('\n'):
            if f':{port}' in line and ('LISTENING' in line or 'ABHÖREN' in line):
                parts = line.split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids_to_kill.append(pid)
        
        if pids_to_kill:
            print(f"📋 Found processes: {pids_to_kill}")
            for pid in pids_to_kill:
                try:
                    subprocess.run(["taskkill", "/PID", pid, "/F"], 
                                  capture_output=True, timeout=5)
                    print(f"✅ Killed process {pid}")
                except Exception as e:
                    print(f"❌ Failed to kill process {pid}: {e}")
        else:
            print(f"✅ No processes found on port {port}")
            
        return len(pids_to_kill) > 0
        
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False

def test_api_on_port(port=8000):
    """Test if API is working on specified port"""
    print(f"🧪 Testing API on port {port}...")
    
    try:
        # Test basic endpoint
        response = requests.get(f"http://127.0.0.1:{port}/", timeout=5)
        if response.status_code == 200:
            print(f"✅ API responding on port {port}")
            
            # Test conversion
            conv_response = requests.get(
                f"http://127.0.0.1:{port}/convert",
                params={"from_currency": "EUR", "to_currency": "USD", "amount": "100"},
                timeout=10
            )
            
            if conv_response.status_code == 200:
                data = conv_response.json()
                print(f"✅ Conversion test successful! {data}")
                print(f"   {data['amount']} {data['from']} = {data['result']} {data['to']}")
                return True
            else:
                print(f"❌ Conversion failed: {conv_response.status_code}")
                print(f"   Response: {conv_response.text}")
                return False
        else:
            print(f"❌ API not responding on port {port}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ No API server running on port {port}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def start_fresh_api(port=8000):
    """Start a fresh API server"""
    print(f"🚀 Starting fresh API server on port {port}...")
    
    try:
        process = subprocess.Popen(
            ["uvicorn", "api_free:app", "--host", "127.0.0.1", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        if test_api_on_port(port):
            print(f"✅ API server started successfully on port {port}")
            return process
        else:
            print("❌ API server failed to start properly")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def main():
    """Main fix function"""
    print("🔧 Port 8000 Fix Tool")
    print("=" * 30)
    
    # Step 1: Kill any existing processes on port 8000
    killed_processes = kill_processes_on_port(8000)
    
    if killed_processes:
        print("⏳ Waiting for processes to fully terminate...")
        time.sleep(2)
    
    print()
    
    # Step 2: Test if anything is still running
    if test_api_on_port(8000):
        print("ℹ️  API is already running and working on port 8000")
        return True
    
    print()
    
    # Step 3: Start fresh API server
    process = start_fresh_api(8000)
    
    if process:
        print("\n🎉 Success! API server is now running properly.")
        print("💡 You can now:")
        print("   1. Launch the GUI: python gui_launcher.py")
        print("   2. Go to Live Currency API tab")
        print("   3. Select Free API mode")
        print("   4. Click Start API Server")
        print("   5. Test currency conversion")
        
        print("\n⚠️  Press Ctrl+C to stop this server when done testing")
        
        try:
            # Keep server running
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
        
        return True
    else:
        print("\n❌ Could not start API server")
        print("💡 Try:")
        print("   1. Restart your computer")
        print("   2. Check if antivirus is blocking Python")
        print("   3. Try running as administrator")
        return False

if __name__ == "__main__":
    try:
        success = main()
    except KeyboardInterrupt:
        print("\n👋 Fix interrupted")
        success = False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        success = False
    
    if not success:
        print("\n💡 Alternative: Use the GUI with automatic port detection")
        print("   The updated GUI will find an available port automatically")
