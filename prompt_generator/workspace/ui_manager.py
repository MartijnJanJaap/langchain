# filename: ui_manager.py
import tkinter as tk
from tkinter import ttk


def apply_styles():
    try:
        style = ttk.Style()
        style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white",
                        borderwidth=0)
        style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)
        style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#222222", borderwidth=0)
    except Exception as e:
        print(f"[ERROR] Failed to apply UI styles: {e}")


class UIFileSelector:
    def __init__(self, parent, workspace_dir, populate_tree_callback, load_subdirectory_callback, toggle_selection_callback):
        self.parent = parent

        # Apply styles
        apply_styles()

        # Set the parent (root window's) background to black
        self.parent.configure(bg="#000000")

        # Input section
        ttk.Label(self.parent, text="Enter additional instructions:",
                  font=("Arial", 12), foreground="white", background="#000000").pack(pady=5)

        self.text_input = tk.Text(self.parent, height=4, width=80, bg="#333333", fg="white",
                                  font=("Arial", 12), insertbackground="lime")
        self.text_input.pack(pady=5, padx=20)

        # Treeview section
        self.tree_frame = tk.Frame(self.parent, bg="#000000", padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create Treeview with dark theme
        self.tree = ttk.Treeview(self.tree_frame, show="tree", selectmode="none", columns=("checked",))

        # Apply styles to Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
        self.style.configure("Treeview.Heading", background="#222222", foreground="white")
        self.style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6, background="#333333")
        
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar with dark theme
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.populate_tree_callback = populate_tree_callback
        self.load_subdirectory_callback = load_subdirectory_callback
        self.toggle_selection_callback = toggle_selection_callback

        self.populate_tree_callback(self.tree)
        self.tree.bind("<<TreeviewOpen>>", self.load_subdirectory_callback)
        self.tree.tag_configure("unchecked", background="#333333")
        self.tree.tag_configure("checked", background="#666666", foreground="#FFBF00")
        self.tree.bind("<ButtonRelease-1>", self.toggle_selection_callback)