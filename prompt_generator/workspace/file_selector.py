# filename: file_selector.py
import os
import tkinter as tk
from tkinter import ttk, messagebox

from prompt_generator.workspace.file_filter import FileFilter
from prompt_generator.workspace.get_last_known_prompt import get_last_known_prompt

class FileSelector:
    def __init__(self, parent, workspace_dir, prompts_dir):
        self.parent = parent
        self.prompts_dir = prompts_dir
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.selected_files = set()
        self.filter = FileFilter()
        self.user_input = ""

        # Set the parent (root window's) background to black
        self.parent.configure(bg="#000000")

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

        self.populate_tree()
        self.tree.bind("<<TreeviewOpen>>", self.load_subdirectory)
        self.tree.tag_configure("unchecked", background="#333333")
        self.tree.tag_configure("checked", background="#666666", foreground="#FFBF00")
        self.tree.bind("<ButtonRelease-1>", self.toggle_selection)

        ttk.Label(self.parent, text="Enter additional instructions:",
                  font=("Arial", 12), foreground="white", background="#000000").pack(pady=5)

        self.text_input = tk.Text(self.parent, height=4, width=80, bg="#333333", fg="white",
                                  font=("Arial", 12), insertbackground="lime")
        self.text_input.pack(pady=5, padx=20)

        last_prompt = get_last_known_prompt(self)
        if last_prompt:
            self.text_input.insert("1.0", last_prompt)

        self.button_frame = tk.Frame(self.parent, bg="#000000")
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.ok_button = ttk.Button(self.button_frame, text="Generate Prompt",
                                    command=self.generate_prompt, style="Dark.TButton")
        self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel",
                                        command=self.cancel_action, style="Dark.TButton")
        self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

        self.apply_styles()

    def cancel_action(self):
        """Cancel action that clears selection and quits."""
        self.selected_files.clear()  # Clear the selected files
        self.user_input = ""  # Optionally, clear any user input as well
        self.parent.quit()

    def apply_styles(self):
        try:
            style = ttk.Style()
            style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white",
                            borderwidth=0)
            style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)
            style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#222222", borderwidth=0)
        except Exception as e:
            print(f"[ERROR] Failed to apply UI styles: {e}")

    def populate_tree(self):
        try:
            entries = sorted(os.listdir(self.workspace_dir))
            for entry in entries:
                full_path = os.path.join(self.workspace_dir, entry)
                if self.filter.is_ignored(full_path):
                    continue
                if os.path.isdir(full_path):
                    folder_id = self.tree.insert("", "end", iid=full_path, text=f"📁 {entry}", open=False, tags="unchecked")
                    self.add_dummy_node(folder_id)
                elif os.path.isfile(full_path):
                    self.tree.insert("", "end", iid=full_path, text=f"📄 {entry}", tags="unchecked")
        except Exception as e:
            print(f"[ERROR] Could not load workspace contents: {e}")

    def add_dummy_node(self, node):
        """Add a dummy node to indicate that a folder has subfolders."""
        self.tree.insert(node, "end", iid=f"{node}_dummy", text="Loading...")

    def remove_dummy_node(self, node):
        """Remove the dummy 'Loading...' node."""
        for child in self.tree.get_children(node):
            if self.tree.item(child, "text") == "Loading...":
                self.tree.delete(child)

    def load_subdirectory(self, event):
        """Dynamically load subfolders only when a folder is expanded."""
        item = self.tree.focus()
        real_path = item if item else ""

        if not os.path.isdir(real_path):
            return

        self.remove_dummy_node(item)

        try:
            subfolders, files = [], []
            for entry in sorted(os.listdir(real_path)):
                full_path = os.path.join(real_path, entry)
                if self.filter.is_ignored(full_path):
                    continue
                if os.path.isdir(full_path):
                    subfolders.append((full_path, os.path.basename(full_path)))
                elif os.path.isfile(full_path):
                    files.append(full_path)

            for full_path, folder_name in subfolders:
                folder_id = self.tree.insert(item, "end", iid=full_path, text=f"📁 {folder_name}", open=False, tags="unchecked")
                self.add_dummy_node(folder_id)

            for file_path in files:
                file_name = os.path.basename(file_path)
                self.tree.insert(item, "end", iid=file_path, text=f"📄 {file_name}", tags="unchecked")

        except PermissionError:
            messagebox.showwarning("Permission Denied", f"Cannot access {real_path}.")
        except Exception as e:
            print(f"[ERROR] Could not load folder '{real_path}': {e}")

    def toggle_selection(self, event):
        item = self.tree.identify_row(event.y)
        if item and self.tree.tag_has("unchecked", item):
            self.tree.item(item, tags="checked")
            self.selected_files.add(item)
        elif item and self.tree.tag_has("checked", item):
            self.tree.item(item, tags="unchecked")
            self.selected_files.remove(item)

    def get_selected_files(self):
        return list(self.selected_files)

    def generate_prompt(self):
        self.user_input = self.text_input.get("1.0", tk.END).strip()
        self.parent.quit()