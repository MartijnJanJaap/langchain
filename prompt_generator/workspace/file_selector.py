import os
import tkinter as tk
from tkinter import messagebox, ttk

from prompt_generator.workspace.file_filter import FileFilter
from prompt_generator.workspace.get_last_known_prompt import get_last_known_prompt
from prompt_generator.workspace.ui_manager import UIFileSelector


def remove_dummy_node(tree, node):
    for child in tree.get_children(node):
        if tree.item(child, "text") == "Loading...":
            tree.delete(child)


def add_dummy_node(tree, node):
    """Add a dummy node to indicate that a folder has subfolders."""
    tree.insert(node, "end", iid=f"{node}_dummy", text="Loading...")


class FileSelector:
    def __init__(self, parent, root_dir):
        self.parent = parent
        self.workspace_dir = os.path.abspath(root_dir + "workspace/")
        self.selected_files = set()
        self.filter = FileFilter()
        self.user_input = ""

        self.ui = UIFileSelector(
            parent,
            self.workspace_dir,
            self.populate_tree,
            self.load_subdirectory,
            self.toggle_selection
        )

        last_prompt = get_last_known_prompt(prompts_dir=root_dir+"prompts/")
        if last_prompt:
            self.ui.text_input.insert("1.0", last_prompt)

        self.button_frame = tk.Frame(self.parent, bg="#000000")
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.ok_button = ttk.Button(
            self.button_frame, text="Generate Prompt",
            command=self.generate_prompt, style="Dark.TButton")
        self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.cancel_button = ttk.Button(
            self.button_frame, text="Cancel",
            command=self.cancel_action, style="Dark.TButton")
        self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

    def cancel_action(self):
        self.selected_files.clear()
        self.user_input = ""
        self.parent.quit()

    def populate_tree(self, tree):
        try:
            entries = sorted(os.listdir(self.workspace_dir))
            for entry in entries:
                full_path = os.path.join(self.workspace_dir, entry)
                if self.filter.is_ignored(full_path):
                    continue
                if os.path.isdir(full_path):
                    folder_id = tree.insert("", "end", iid=full_path, text=f"\U0001F4C1 {entry}", open=False, tags="unchecked")
                    add_dummy_node(tree, folder_id)
                elif os.path.isfile(full_path):
                    tree.insert("", "end", iid=full_path, text=f"\U0001F4C4 {entry}", tags="unchecked")
        except Exception as e:
            print(f"[ERROR] Could not load workspace contents: {e}")

    def load_subdirectory(self, event=None):
        item = self.ui.tree.focus()
        real_path = item if item else ""

        if not os.path.isdir(real_path):
            return

        remove_dummy_node(self.ui.tree, item)

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
                folder_id = self.ui.tree.insert(item, "end", iid=full_path, text=f"\U0001F4C1 {folder_name}", open=False, tags="unchecked")
                add_dummy_node(self.ui.tree, folder_id)

            for file_path in files:
                file_name = os.path.basename(file_path)
                self.ui.tree.insert(item, "end", iid=file_path, text=f"\U0001F4C4 {file_name}", tags="unchecked")

        except PermissionError:
            messagebox.showwarning("Permission Denied", f"Cannot access {real_path}.")
        except Exception as e:
            print(f"[ERROR] Could not load folder '{real_path}': {e}")

    def toggle_selection(self, event):
        item = self.ui.tree.identify_row(event.y)
        if item and self.ui.tree.tag_has("unchecked", item):
            self.ui.tree.item(item, tags="checked")
            self.selected_files.add(item)
        elif item and self.ui.tree.tag_has("checked", item):
            self.ui.tree.item(item, tags="unchecked")
            self.selected_files.remove(item)

    def get_selected_files(self):
        return list(self.selected_files)

    def generate_prompt(self):
        self.user_input = self.ui.text_input.get("1.0", tk.END).strip()
        self.parent.quit()
