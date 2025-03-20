# filename: file_selector.py

import os
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

from prompt_generator.workspace.file_filter import FileFilter
from prompt_generator.workspace.ui_manager import UIFileSelector
from prompt_generator.workspace.auto_select_files_based_on_prompt import OpenAIIntegration

def remove_dummy_node(tree, node):
    dummy = f"{node}_dummy"
    if tree.exists(dummy):
        print(f"Removing dummy node for: {node}")
        tree.delete(dummy)

def add_dummy_node(tree, node):
    """Add a dummy node to indicate that a folder has subfolders."""
    print(f"Adding dummy node for: {node}")
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

        self.button_frame = tk.Frame(self.parent, bg="#000000")
        self.button_frame.pack(fill=tk.X, padx=0, pady=10)

        self.auto_select_button = ttk.Button(
            self.button_frame, text="Auto Select",
            command=self.auto_select_files, style="Dark.TButton")
        self.auto_select_button.pack(side=tk.LEFT, expand=True, padx=5, pady=0)

        self.ok_button = ttk.Button(
            self.button_frame, text="Generate Prompt",
            command=self.generate_prompt, style="Dark.TButton")
        self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.cancel_button = ttk.Button(
            self.button_frame, text="Cancel",
            command=self.cancel_action, style="Dark.TButton")
        self.cancel_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    def auto_select_files(self):
        self.user_input = self.ui.text_input.get("1.0", tk.END).strip()
        root_dir = self.workspace_dir
        openai_integration = OpenAIIntegration()
        relevant_files = openai_integration.get_files_which_are_related_to_prompt(self.user_input, root_dir)

        # Use Path().resolve() and replace '\\' with '\' for single backslashes
        relevant_files = [str(Path(file).resolve()).replace("\\\\", "\\") for file in relevant_files]
        print(f"Relevant files to be auto-selected: {relevant_files}")

        if relevant_files:
            print("Attempting to auto-select files based on AI prompt analysis:")
            self.select_files_programmatically(relevant_files)
        else:
            print("No files were selected by AI prompt analysis.")

        self.ui.tree.update_idletasks()

    def cancel_action(self):
        self.selected_files.clear()
        self.user_input = ""
        self.parent.quit()

    def populate_tree(self, tree):
        try:
            entries = sorted(os.listdir(self.workspace_dir))
            for entry in entries:
                full_path = os.path.join(self.workspace_dir, entry)
                print(f"Inserting tree item: {full_path}")
                if self.filter.is_ignored(full_path):
                    print(f"Ignored: {full_path}")
                    continue
                if os.path.isdir(full_path):
                    folder_id = tree.insert("", "end", iid=full_path, text=f"\U0001F4C1 {entry}", open=False, tags="unchecked")
                    add_dummy_node(tree, folder_id)
                elif os.path.isfile(full_path):
                    tree.insert("", "end", iid=full_path, text=f"\U0001F4C4 {entry}", tags="unchecked")
        except Exception as e:
            print(f"[ERROR] Could not load workspace contents: {e}")

    def load_subdirectory(self, item):
        if not os.path.isdir(item):
            print(f"Skipping non-directory: {item}")
            return

        print(f"Loading subdirectory: {item}")
        remove_dummy_node(self.ui.tree, item)

        try:
            subfolders, files = [], []
            for entry in sorted(os.listdir(item)):
                full_path = os.path.join(item, entry)
                if self.filter.is_ignored(full_path):
                    print(f"Ignored: {full_path}")
                    continue
                if os.path.isdir(full_path):
                    subfolders.append((full_path, os.path.basename(full_path)))
                elif os.path.isfile(full_path):
                    files.append(full_path)

            for full_path, folder_name in subfolders:
                print(f"Inserting subfolder: {full_path}")
                folder_id = self.ui.tree.insert(item, "end", iid=full_path, text=f"\U0001F4C1 {folder_name}", open=False, tags="unchecked")
                add_dummy_node(self.ui.tree, folder_id)

            for file_path in files:
                print(f"Inserting file: {file_path}")
                file_name = os.path.basename(file_path)
                self.ui.tree.insert(item, "end", iid=file_path, text=f"\U0001F4C4 {file_name}", tags="unchecked")

        except PermissionError:
            messagebox.showwarning("Permission Denied", f"Cannot access {item}.")
        except Exception as e:
            print(f"[ERROR] Could not load folder '{item}': {e}")

    def toggle_selection(self, event):
        item = self.ui.tree.identify_row(event.y)
        if item and self.ui.tree.tag_has("unchecked", item):
            self.ui.tree.item(item, tags="checked")
            self.selected_files.add(item)
            print(f"Item selected: {item}")
        elif item and self.ui.tree.tag_has("checked", item):
            self.ui.tree.item(item, tags="unchecked")
            self.selected_files.remove(item)
            print(f"Item unselected: {item}")

    def get_selected_files(self):
        return list(self.selected_files)

    def generate_prompt(self):
        self.user_input = self.ui.text_input.get("1.0", tk.END).strip()
        print(f"Generated prompt: {self.user_input}")
        self.parent.quit()

    def select_files_programmatically(self, file_list):
        # Normalize the paths in file_list for consistency
        file_list = [str(Path(file).resolve()).replace("\\\\", "\\") for file in file_list]

        def traverse_and_select(node):
            print(f"Traversing node: {node}")
            if os.path.isdir(node):
                self.load_subdirectory(node)

            children = self.ui.tree.get_children(node)
            for child in children:
                full_path = str(Path(child).resolve()).replace("\\\\", "\\")  # Normalize path
                print(full_path)

                if full_path in file_list:
                    print(f"Selecting file: {full_path}")
                    self.ui.tree.item(child, tags="checked")
                    self.selected_files.add(full_path)
                    file_list.remove(full_path)

                if self.ui.tree.exists(child) and os.path.isdir(full_path):
                    traverse_and_select(child)

        # Initial traversal for the root children
        root_items = self.ui.tree.get_children()
        for root_item in root_items:
            full_path = str(Path(root_item).resolve()).replace("\\\\", "\\")  # Normalize path
            print(full_path)

            if full_path in file_list:
                print(f"Selecting file: {full_path}")
                self.ui.tree.item(root_item, tags="checked")
                self.selected_files.add(full_path)
                file_list.remove(full_path)

            traverse_and_select(root_item)

        if file_list:
            print(f"Some files were not found for selection: {file_list}")
