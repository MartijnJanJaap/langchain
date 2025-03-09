# filename: file_selector.py
import os
import tkinter as tk
from tkinter import ttk, messagebox

class FileSelector:
    def __init__(self, parent, workspace_dir, prompts_dir):
        self.parent = parent
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.prompts_dir = os.path.abspath(prompts_dir)  # Add prompts_dir argument

        # Continue with the rest of the initialization code...

        self.selected_files = set()

        self.tree_frame = tk.Frame(self.parent, bg="#333333", padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create Treeview with dark theme
        self.tree = ttk.Treeview(self.tree_frame, show="tree")

        # Apply styles to Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
        self.style.configure("Treeview.Heading", background="#222222", foreground="white")  # Fix header color

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar with dark theme
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.populate_tree()
        self.tree.bind("<<TreeviewOpen>>", self.load_subdirectory)
        self.tree.bind("<ButtonRelease-1>", self.toggle_selection)

        self.apply_styles()

    # rest of the class methods...