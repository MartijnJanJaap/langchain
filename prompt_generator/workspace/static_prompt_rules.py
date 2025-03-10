# filename: static_prompt_rules.py
import tkinter as tk

def get_static_rules():
    rules = [
        "Always return full files because the code you output is automatically copied."
    ]
    return "\n".join(rules)

class StaticRulesUI:
    def __init__(self, parent):
        self.parent = parent
        self.rules_variables = []

        # Apply styles directly within the class
        self.style = {
            'bg': '#000000',    # Dark background
            'fg': 'white',      # White text
            'selectcolor': '#333333'  # Dark select color
        }
        
        self.font_settings = ('Arial', 14)  # Set font and size
        self.parent.configure(bg=self.style['bg'])

        # Create a section in the UI for static rules
        self.create_static_rules_checkboxes()

    def create_static_rules_checkboxes(self):
        rules = get_static_rules().split("\n")
        for rule in rules:
            var = tk.BooleanVar(value=True)  # Set the default value to True
            chk = tk.Checkbutton(self.parent, text=rule, variable=var,
                                 bg=self.style['bg'], fg=self.style['fg'],
                                 selectcolor=self.style['selectcolor'], font=self.font_settings,
                                 anchor='w', pady=2)
            chk.pack(fill='x')
            self.rules_variables.append(var)

    def get_selected_rules(self):
        selected_rules = []
        rules = get_static_rules().split("\n")
        for i, var in enumerate(self.rules_variables):
            if var.get():
                selected_rules.append(rules[i])
        return selected_rules