#!/usr/bin/env python3
"""
Debug script to test if the text widget in the GUI is working
"""

import tkinter as tk
from tkinter import ttk, messagebox

def test_text_widget():
    """Test if we can write to the text widget"""
    try:
        # Clear and test basic writing
        api_result.delete(1.0, tk.END)
        api_result.insert(tk.END, "🧪 Testing text widget...\n")
        api_result.insert(tk.END, "✅ Basic text insertion works!\n")
        
        # Test formatted text like the main GUI
        test_data = {
            'amount': 100.0,
            'from': 'EUR', 
            'to': 'USD',
            'result': 116.0,
            'info': {'rate': 1.16}
        }
        
        cached_status = "Live"
        result_text = f"""✅ {cached_status} Currency Conversion:
{test_data['amount']} {test_data['from']} = {test_data['result']:.2f} {test_data['to']}
Exchange Rate: {test_data['info']['rate']:.4f}
{'-'*40}
"""
        
        api_result.insert(tk.END, result_text)
        api_result.see(tk.END)
        
        messagebox.showinfo("Success", "Text widget is working correctly!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Text widget error: {str(e)}")

def test_api_simulation():
    """Simulate the exact API response handling"""
    try:
        api_result.delete(1.0, tk.END)
        
        # Simulate progress message
        api_result.insert(tk.END, "🔄 Converting 100 EUR to USD...\n")
        api_result.see(tk.END)
        root.update()
        
        # Simulate API response (like from your logs)
        simulated_response = {
            'cached': True,
            'from': 'EUR',
            'to': 'USD', 
            'amount': 100.0,
            'result': 116.0,
            'info': {'rate': 1.16}
        }
        
        # Use exact same code as main GUI
        cached_status = "Cached" if simulated_response.get("cached", False) else "Live"
        result_text = f"""✅ {cached_status} Currency Conversion:
{simulated_response['amount']} {simulated_response['from']} = {simulated_response['result']:.2f} {simulated_response['to']}
Exchange Rate: {simulated_response['info']['rate']:.4f}
{'-'*40}
"""
        api_result.insert(tk.END, result_text)
        api_result.see(tk.END)
        
        messagebox.showinfo("Success", "API simulation successful!")
        
    except Exception as e:
        messagebox.showerror("Error", f"API simulation error: {str(e)}")

def check_widget_state():
    """Check the state of the text widget"""
    try:
        state = api_result.cget('state')
        height = api_result.cget('height')
        width = api_result.cget('width')
        bg = api_result.cget('bg')
        fg = api_result.cget('fg')
        
        info = f"""📊 Text Widget Information:
State: {state}
Height: {height}
Width: {width}
Background: {bg}
Foreground: {fg}
"""
        
        api_result.delete(1.0, tk.END)
        api_result.insert(tk.END, info)
        
        # Check if widget is visible
        if api_result.winfo_viewable():
            api_result.insert(tk.END, "✅ Widget is visible\n")
        else:
            api_result.insert(tk.END, "❌ Widget is not visible\n")
            
        # Check if widget has focus capability
        if api_result.focus_get() == api_result:
            api_result.insert(tk.END, "✅ Widget can receive focus\n")
        else:
            api_result.insert(tk.END, "ℹ️  Widget does not have focus\n")
            
    except Exception as e:
        messagebox.showerror("Error", f"Widget state check error: {str(e)}")

def clear_widget():
    """Clear the text widget"""
    api_result.delete(1.0, tk.END)

# Create test GUI
root = tk.Tk()
root.title("Text Widget Debug Tool")
root.geometry("800x600")
root.configure(bg='#2c3e50')

# Title
title_label = ttk.Label(root, text="Text Widget Debug Tool", font=('Arial', 16, 'bold'))
title_label.pack(pady=10)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Test Basic Text", command=test_text_widget).pack(side='left', padx=5)
ttk.Button(button_frame, text="Test API Simulation", command=test_api_simulation).pack(side='left', padx=5)
ttk.Button(button_frame, text="Check Widget State", command=check_widget_state).pack(side='left', padx=5)
ttk.Button(button_frame, text="Clear", command=clear_widget).pack(side='left', padx=5)

# Create the EXACT same text widget as in the main GUI
api_result = tk.Text(root, height=8, width=60, font=('Arial', 12),
                    bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1')
api_result.pack(pady=20)

# Add scrollbar
scrollbar = ttk.Scrollbar(root, orient='vertical', command=api_result.yview)
scrollbar.pack(side='right', fill='y')
api_result.config(yscrollcommand=scrollbar.set)

# Initial test
api_result.insert(tk.END, "🔧 Text Widget Debug Tool Ready\n")
api_result.insert(tk.END, "Click buttons above to test functionality\n")
api_result.insert(tk.END, "This uses the EXACT same text widget as your main GUI\n")

if __name__ == "__main__":
    print("🔧 Starting Text Widget Debug Tool...")
    root.mainloop()
