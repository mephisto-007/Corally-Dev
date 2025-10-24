#!/usr/bin/env python3
"""
Fix script for GUI output issues
This will help diagnose and fix why the GUI doesn't show output
"""

import tkinter as tk
from tkinter import ttk
import requests
import subprocess
import time

def start_api_server():
    """Start the API server for testing"""
    print("🚀 Starting API server...")
    try:
        process = subprocess.Popen(
            ["uvicorn", "api_free:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)  # Wait for server to start
        
        # Test if server is running
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API server started successfully")
            return process
        else:
            print("❌ API server failed to start properly")
            process.terminate()
            return None
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def test_gui_output_widget():
    """Test the GUI output widget specifically"""
    
    def test_basic_output():
        """Test basic text output"""
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "🧪 Testing basic output...\n")
            output_text.insert(tk.END, "✅ Basic text insertion works!\n")
            output_text.see(tk.END)
            status_label.config(text="✅ Basic output test passed")
        except Exception as e:
            status_label.config(text=f"❌ Basic output test failed: {e}")
    
    def test_formatted_output():
        """Test formatted output like the main GUI"""
        try:
            output_text.delete(1.0, tk.END)
            
            # Simulate the exact format from main GUI
            result_text = f"""✅ Live Currency Conversion:
100.0 EUR = 116.00 USD
Exchange Rate: 1.1600
{'-'*40}
"""
            output_text.insert(tk.END, result_text)
            output_text.see(tk.END)
            status_label.config(text="✅ Formatted output test passed")
        except Exception as e:
            status_label.config(text=f"❌ Formatted output test failed: {e}")
    
    def test_api_connection():
        """Test actual API connection and output"""
        try:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "🔄 Testing API connection...\n")
            root.update()
            
            # Test API
            response = requests.get(
                "http://127.0.0.1:8000/convert",
                params={"from_currency": "EUR", "to_currency": "USD", "amount": "100"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                cached_status = "Cached" if data.get("cached", False) else "Live"
                
                result_text = f"""✅ {cached_status} Currency Conversion:
{data['amount']} {data['from']} = {data['result']:.2f} {data['to']}
Exchange Rate: {data['info']['rate']:.4f}
{'-'*40}
"""
                output_text.insert(tk.END, result_text)
                output_text.see(tk.END)
                status_label.config(text="✅ API connection test passed")
            else:
                output_text.insert(tk.END, f"❌ API Error: {response.status_code}\n")
                status_label.config(text="❌ API returned error")
                
        except requests.exceptions.ConnectionError:
            output_text.insert(tk.END, "❌ Cannot connect to API server\n")
            output_text.insert(tk.END, "💡 Make sure API server is running on port 8000\n")
            status_label.config(text="❌ API server not running")
        except Exception as e:
            output_text.insert(tk.END, f"❌ API test failed: {str(e)}\n")
            status_label.config(text=f"❌ API test failed: {e}")
    
    def clear_output():
        """Clear the output"""
        output_text.delete(1.0, tk.END)
        status_label.config(text="🧹 Output cleared")
    
    def check_widget_properties():
        """Check text widget properties"""
        try:
            output_text.delete(1.0, tk.END)
            
            props = f"""📊 Text Widget Properties:
State: {output_text.cget('state')}
Height: {output_text.cget('height')}
Width: {output_text.cget('width')}
Background: {output_text.cget('bg')}
Foreground: {output_text.cget('fg')}
Font: {output_text.cget('font')}
Wrap: {output_text.cget('wrap')}
"""
            output_text.insert(tk.END, props)
            
            # Check visibility
            if output_text.winfo_viewable():
                output_text.insert(tk.END, "✅ Widget is visible\n")
            else:
                output_text.insert(tk.END, "❌ Widget is not visible\n")
            
            status_label.config(text="✅ Widget properties checked")
            
        except Exception as e:
            status_label.config(text=f"❌ Property check failed: {e}")
    
    # Create test GUI
    root = tk.Tk()
    root.title("GUI Output Debug Tool")
    root.geometry("900x700")
    root.configure(bg='#2c3e50')
    
    # Title
    title_label = ttk.Label(root, text="GUI Output Debug Tool", 
                           font=('Arial', 18, 'bold'))
    title_label.pack(pady=10)
    
    # Instructions
    instructions = ttk.Label(root, text="This tool tests the EXACT same text widget as your main GUI", 
                            font=('Arial', 12))
    instructions.pack(pady=5)
    
    # Status
    status_label = ttk.Label(root, text="🔧 Ready to test", 
                            font=('Arial', 12, 'bold'))
    status_label.pack(pady=10)
    
    # Buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    ttk.Button(button_frame, text="Test Basic Output", command=test_basic_output).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Test Formatted Output", command=test_formatted_output).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Test API Connection", command=test_api_connection).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Check Properties", command=check_widget_properties).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Clear", command=clear_output).pack(side='left', padx=5)
    
    # Create EXACT same text widget as main GUI
    result_label = ttk.Label(root, text="Output Area (Same as Main GUI):", font=('Arial', 12, 'bold'))
    result_label.pack(pady=(20, 5))
    
    output_text = tk.Text(root, height=8, width=60, font=('Arial', 12),
                         bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1',
                         wrap=tk.WORD, state=tk.NORMAL)
    output_text.pack(pady=20, padx=20, fill='both', expand=True)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=output_text.yview)
    scrollbar.pack(side='right', fill='y')
    output_text.config(yscrollcommand=scrollbar.set)
    
    # Initial message
    output_text.insert(tk.END, "💡 GUI Output Debug Tool Ready\n")
    output_text.insert(tk.END, "Click buttons above to test different scenarios\n")
    output_text.insert(tk.END, f"{'-'*50}\n")
    
    return root

def main():
    """Main function"""
    print("🔧 GUI Output Fix Tool")
    print("=" * 30)
    
    # Check if API server is needed
    try:
        requests.get("http://127.0.0.1:8000/", timeout=2)
        print("✅ API server is already running")
        server_process = None
    except Exception as e:
        print(f"❌ API server check failed: {e}")
        print("🚀 Starting API server...")
        server_process = start_api_server()
        if not server_process:
            print("❌ Could not start API server")
            print("💡 You can still test the GUI output widget")
    
    print("\n🖥️  Starting GUI debug tool...")
    
    try:
        root = test_gui_output_widget()
        
        def on_closing():
            if server_process:
                print("🛑 Stopping API server...")
                server_process.terminate()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
