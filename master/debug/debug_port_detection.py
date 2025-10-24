#!/usr/bin/env python3
"""
Debug script to test port detection
"""

import subprocess

def debug_netstat():
    """Debug netstat output"""
    print("🔍 Running netstat -ano...")
    
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print("📄 Full netstat output:")
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if ':8000' in line:
                print(f"Line {i}: {repr(line)}")
                print(f"         {line}")
                
                # Check each listening indicator
                listening_indicators = ['LISTENING', 'ABHÖREN', 'LISTEN', 'ABH?REN', 'ABHOREN', 'ABH™REN']
                for indicator in listening_indicators:
                    if indicator in line:
                        print(f"   ✅ Found indicator: {indicator}")
                        parts = line.split()
                        print(f"   📋 Parts: {parts}")
                        if parts:
                            pid = parts[-1]
                            print(f"   🆔 PID: {pid} (is digit: {pid.isdigit()})")
                        break
                else:
                    print("   ❌ No listening indicators found")
                    print(f"   📋 Parts: {line.split()}")
                
                print()
        
        if not any(':8000' in line for line in lines):
            print("❌ No lines containing :8000 found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_pid():
    """Test the get_pid_on_port function"""
    print("\n🧪 Testing get_pid_on_port function...")
    
    # Import the function from manage_api_server
    import sys
    sys.path.append('.')
    
    try:
        from manage_api_server import get_pid_on_port
        pid = get_pid_on_port(8000, debug=True)
        print(f"🆔 Result: {pid}")
    except Exception as e:
        print(f"❌ Error importing/running function: {e}")

if __name__ == "__main__":
    debug_netstat()
    test_get_pid()
