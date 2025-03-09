# filename: style_manager.py
from tkinter import ttk

def apply_default_styles():
    """Apply default styles to Tkinter app."""
    try:
        style = ttk.Style()
        style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
        style.configure("Dark.TCheckbutton", foreground="white", background="#222222", font=("Arial", 12))
        style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)
        style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#222222")
    except Exception as e:
        print(f"[ERROR] Failed to apply UI styles: {e}")