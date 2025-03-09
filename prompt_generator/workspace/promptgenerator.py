# filename: C:\projects\portfoliomanager\prompt_generator\workspace\promptgenerator.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from prompt_generator.workspace.file_selector import FileSelector

def get_file_structure_string(directory):
    """Recursively build the file structure as a string."""
    file_structure = []
    for dirpath, dirnames, filenames in os.walk(directory):
        level = dirpath.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        file_structure.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = ' ' * 4 * (level + 1)
        for filename in filenames:
            file_structure.append(f"{subindent}{filename}")
    return "\n".join(file_structure)

class PromptGenerator:
    def __init__(self, root, workspace_dir, prompts_dir):
        try:
            self.root = root
            self.root.title("Generate AI Prompt")
            self.workspace_dir = workspace_dir
            self.prompts_dir = prompts_dir
            self.selected_files = []
            self.user_input = ""

            self.root.geometry("850x600")
            self.root.configure(bg="#222222")

            ttk.Label(self.root, text="Select files to include:",
                      font=("Arial", 14, "bold"), foreground="white", background="#222222").pack(pady=10)

            self.file_selector = FileSelector(self.root, workspace_dir)  # Using FileSelector

            ttk.Label(self.root, text="Enter additional instructions:",
                      font=("Arial", 12), foreground="white", background="#222222").pack(pady=5)

            self.text_input = tk.Text(self.root, height=4, width=80, bg="#333333", fg="white",
                                      font=("Arial", 12), insertbackground="lime")
            self.text_input.pack(pady=5, padx=20)

            last_prompt = self.get_last_known_prompt()
            if last_prompt:
                self.text_input.insert("1.0", last_prompt)

            self.button_frame = tk.Frame(self.root, bg="#222222")
            self.button_frame.pack(fill=tk.X, padx=20, pady=10)

            self.ok_button = ttk.Button(self.button_frame, text="Generate Prompt",
                                        command=self.generate_prompt, style="Dark.TButton")
            self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

            self.cancel_button = ttk.Button(self.button_frame, text="Cancel",
                                            command=root.quit, style="Dark.TButton")
            self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

            self.apply_styles()
        except Exception as e:
            print(f"[ERROR] Failed to initialize UI: {e}")

    def get_last_known_prompt(self):
        try:
            if not os.path.exists(self.prompts_dir):
                print("No prompts directory exists")
                return ""

            prompt_files = [os.path.join(self.prompts_dir, f) for f in os.listdir(self.prompts_dir) if f.endswith(".txt")]
            if not prompt_files:
                return ""

            latest_prompt_file = max(prompt_files, key=os.path.getctime)

            with open(latest_prompt_file, "r", encoding="utf-8") as f:
                return f.read()

        except Exception as e:
            print(f"[ERROR] Failed to retrieve last known prompt: {e}")
            return ""

    def generate_prompt(self):
        selected_files = self.file_selector.get_selected_files()
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file!")
            return

        self.selected_files = selected_files
        self.user_input = self.text_input.get("1.0", tk.END).strip()
        self.root.quit()
        self.root.destroy()

    def apply_styles(self):
        try:
            style = ttk.Style()
            style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
            style.configure("Dark.TCheckbutton", foreground="white", background="#222222", font=("Arial", 12))
            style.configure("Dark.TButton", font=("Arial", 12, "bold"), padding=6)
            style.configure("Vertical.TScrollbar", background="#333333", troughcolor="#222222")
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

def save_user_input(prompts_dir, prompt_text):
    try:
        os.makedirs(prompts_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(prompts_dir, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to save prompt: {e}")
        return None

def generate_full_prompt(workspace_dir, prompts_dir):
    try:
        root = tk.Tk()
        selector = PromptGenerator(root, workspace_dir, prompts_dir)
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

    file_structure = get_file_structure_string(workspace_dir)
    prompt += "### Workspace File Structure:\n" + file_structure + "\n"

    if selector.user_input:
        prompt += f"### Additional Instructions:\n{selector.user_input}\n"

    user_prompt_file = save_user_input(prompts_dir, selector.user_input)
    if user_prompt_file:
        print(f"user prompt saved to: {user_prompt_file}")
    else:
        print("[ERROR] Prompt could not be saved.")

    return prompt

def main():
    workspace_dir = r"C:\projects\portfoliomanager\prompt_generator\workspace"
    prompts_dir = r"C:\projects\portfoliomanager\prompt_generator\prompts"
    generate_full_prompt(workspace_dir, prompts_dir)

if __name__ == "__main__":
    main()