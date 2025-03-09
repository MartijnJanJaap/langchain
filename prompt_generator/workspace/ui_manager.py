# filename: ui_manager.py
import tkinter as tk
from tkinter import ttk

class UIManager:
    def __init__(self, root, file_selector_callback, generate_prompt_callback, cancel_callback):
        self.root = root
        self.file_selector_callback = file_selector_callback
        self.generate_prompt_callback = generate_prompt_callback
        self.cancel_callback = cancel_callback

    def setup_ui(self):
        self.root.title("Generate AI Prompt")
        self.root.geometry("850x600")
        self.root.configure(bg="#222222")

        ttk.Label(self.root, text="Select files to include:",
                  font=("Arial", 14, "bold"), foreground="white", background="#222222").pack(pady=10)

        self.file_selector = self.file_selector_callback(self.root)

        ttk.Label(self.root, text="Enter additional instructions:",
                  font=("Arial", 12), foreground="white", background="#222222").pack(pady=5)

        self.text_input = tk.Text(self.root, height=4, width=80, bg="#333333", fg="white",
                                  font=("Arial", 12), insertbackground="lime")
        self.text_input.pack(pady=5, padx=20)

        self.button_frame = tk.Frame(self.root, bg="#222222")
        self.button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.ok_button = ttk.Button(self.button_frame, text="Generate Prompt",
                                    command=self.generate_prompt_callback, style="Dark.TButton")
        self.ok_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel",
                                        command=self.cancel_callback, style="Dark.TButton")
        self.cancel_button.pack(side=tk.RIGHT, expand=True, padx=5, pady=5)

    def get_user_input(self):
        return self.text_input.get("1.0", tk.END).strip()

    def set_initial_prompt(self, prompt_text):
        if prompt_text:
            self.text_input.insert("1.0", prompt_text)