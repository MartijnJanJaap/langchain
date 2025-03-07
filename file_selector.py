import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FileSelector:
    def __init__(self, root, workspace_dir):
        try:
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

            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            self.file_list = self.list_files(workspace_dir)
            self.file_vars = {}

            for file in self.file_list:
                var = tk.BooleanVar()
                check = ttk.Checkbutton(self.scrollable_frame, text=file, variable=var, style="Dark.TCheckbutton")
                check.pack(anchor="w", padx=10, pady=3)
                self.file_vars[file] = var

            ttk.Label(self.root, text="Enter additional instructions:", font=("Arial", 12), foreground="white", background="#222222").pack(pady=5)

            self.text_input = tk.Text(self.root, height=4, width=80, bg="#333333", fg="white", font=("Arial", 12))
            self.text_input.pack(pady=5, padx=20)

            last_prompt = self.get_last_known_prompt()
            if last_prompt:
                self.text_input.insert("1.0", last_prompt)

            self.button_frame = tk.Frame(self.root, bg="#222222")
            self.button_frame.pack(fill=tk.X, padx=20, pady=10)

            self.select_all_var = tk.BooleanVar()
            self.select_all_button = ttk.Checkbutton(self.button_frame, text="Select All", variable=self.select_all_var, command=self.toggle_select_all, style="Dark.TCheckbutton")
            self.select_all_button.pack(side=tk.LEFT, padx=5, pady=5)

            self.ok_button = ttk.Button(self.button_frame, text="Generate Prompt", command=self.generate_prompt, style="Dark.TButton")
            self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

            self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=root.quit, style="Dark.TButton")
            self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

            self.apply_styles()
        except Exception as e:
            print(f"[ERROR] Failed to initialize UI: {e}")

    def get_last_known_prompt(self):
        """Retrieve the last known prompt from the latest saved file in the 'prompts' directory."""
        try:
            prompts_dir = "prompts"
            if not os.path.exists(prompts_dir):
                return ""

            prompt_files = [os.path.join(prompts_dir, f) for f in os.listdir(prompts_dir) if f.endswith(".txt")]
            if not prompt_files:
                return ""

            latest_prompt_file = max(prompt_files, key=os.path.getctime)

            with open(latest_prompt_file, "r", encoding="utf-8") as f:
                content = f.read()

            if "### Additional Instructions:" in content:
                return content.split("### Additional Instructions:")[-1].strip()

            return ""
        except Exception as e:
            print(f"[ERROR] Failed to retrieve last known prompt: {e}")
            return ""

    def list_files(self, directory):
        try:
            file_list = []
            for root, _, files in os.walk(directory):
                if "__pycache__" in root:
                    continue
                for file in files:
                    if file.endswith(".pyc"):
                        continue
                    file_list.append(os.path.join(root, file))
            return file_list
        except Exception as e:
            print(f"[ERROR] Failed to list files in directory '{directory}': {e}")
            return []

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
        try:
            style = ttk.Style()
            style.configure("Dark.TCheckbutton", foreground="white", background="#333333", font=("Arial", 12))
            style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)
        except Exception as e:
            print(f"[ERROR] Failed to apply UI styles: {e}")

def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="ISO-8859-1") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="windows-1252") as f:
                    return f.read()
            except Exception as e:
                print(f"[ERROR] Failed to read file '{file_path}': {e}")
                return f"(Error reading file: {e})"
    except Exception as e:
        print(f"[ERROR] Unexpected error reading file '{file_path}': {e}")
        return f"(Error reading file: {e})"

def save_prompt(prompt_text):
    try:
        prompts_dir = "prompts"
        os.makedirs(prompts_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(prompts_dir, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to save prompt: {e}")
        return None

def generate_full_prompt(workspace_dir):
    try:
        root = tk.Tk()
        selector = FileSelector(root, workspace_dir)
        root.mainloop()
    except Exception as e:
        print(f"[ERROR] Failed to initialize file selector: {e}")
        return None

    if not selector.selected_files:
        print("[INFO] No files selected, exiting prompt generation.")
        return None

    prompt = "Here are the selected files and their contents:\n\n"
    for file_path in selector.selected_files:
        file_content = read_file_content(file_path)
        prompt += f"### File: {file_path}\n{file_content}\n\n"

    if selector.user_input:
        prompt += f"### Additional Instructions:\n{selector.user_input}\n"

    prompt_file = save_prompt(prompt)
    if prompt_file:
        print(f"Prompt saved to: {prompt_file}")
    else:
        print("[ERROR] Prompt could not be saved.")

    return prompt