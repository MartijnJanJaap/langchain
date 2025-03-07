import os
import tkinter as tk
from tkinter import ttk, messagebox

class FileSelector:
    def __init__(self, root, workspace_dir):
        self.root = root
        self.root.title("Generate AI Prompt")
        self.workspace_dir = workspace_dir
        self.selected_files = []
        self.user_input = ""

        self.root.geometry("850x600")
        self.root.configure(bg="#222222")

        ttk.Label(self.root, text="Select files to include:", font=("Arial", 14, "bold"), foreground="white", background="#222222").pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#333333", padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.frame, bg="#333333", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#333333")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.file_list = self.list_files(workspace_dir)
        self.file_vars = {}

        for file in self.file_list:
            var = tk.BooleanVar()
            check = ttk.Checkbutton(
                self.scrollable_frame,
                text=file,
                variable=var,
                style="Dark.TCheckbutton"
            )
            check.pack(anchor="w", padx=10, pady=3)
            self.file_vars[file] = var

        ttk.Label(self.root, text="Enter additional instructions:", font=("Arial", 12), foreground="white", background="#222222").pack(pady=5)

        self.text_input = tk.Text(self.root, height=4, width=80, bg="#333333", fg="white", font=("Arial", 12))
        self.text_input.pack(pady=5, padx=20)

        self.button_frame = tk.Frame(self.root, bg="#222222")
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.select_all_var = tk.BooleanVar()
        self.select_all_button = ttk.Checkbutton(self.button_frame, text="Select All", variable=self.select_all_var, command=self.toggle_select_all, style="Dark.TCheckbutton")
        self.select_all_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.ok_button = ttk.Button(self.button_frame, text="Generate Prompt", command=self.generate_prompt, style="Dark.TButton")
        self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=root.quit, style="Dark.TButton")
        self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

        self.apply_styles()  # Ensure this function exists before calling it

    def list_files(self, directory):
        file_list = []
        for root, _, files in os.walk(directory):
            if "__pycache__" in root:
                continue
            for file in files:
                if file.endswith(".pyc"):
                    continue
                file_list.append(os.path.join(root, file))
        return file_list

    def toggle_select_all(self):
        is_selected = self.select_all_var.get()
        for var in self.file_vars.values():
            var.set(is_selected)

    def generate_prompt(self):
        selected_files = [file for file, var in self.file_vars.items() if var.get()]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file!")
            return

        self.selected_files = selected_files
        self.user_input = self.text_input.get("1.0", tk.END).strip()

        self.root.quit()

    def apply_styles(self):
        style = ttk.Style()
        style.configure("Dark.TCheckbutton", foreground="white", background="#333333", font=("Arial", 12))
        style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)

def generate_full_prompt(workspace_dir):
    root = tk.Tk()
    selector = FileSelector(root, workspace_dir)
    root.mainloop()

    if not selector.selected_files:
        return None

    prompt = "Here are the selected files and their contents:\n\n"
    for file_path in selector.selected_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            prompt += f"### File: {file_path}\n{file_content}\n\n"
        except Exception as e:
            prompt += f"### File: {file_path}\n(Error reading file: {e})\n\n"

    if selector.user_input:
        prompt += f"### Additional Instructions:\n{selector.user_input}\n"

    return prompt
