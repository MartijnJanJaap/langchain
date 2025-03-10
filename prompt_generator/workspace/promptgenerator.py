# filename: promptgenerator.py
import tkinter as tk

from prompt_generator.workspace.file_selector import FileSelector
from prompt_generator.workspace.static_prompt_rules import StaticRulesUI
from prompt_generator.workspace.file_structure_generator import FileStructureGenerator
from prompt_generator.workspace.prompt_file_manager import save_user_input
from prompt_generator.workspace.read_file_content import read_file_content

def generate_full_prompt(root_dir):
    workspace_dir = root_dir + "/workspace/"
    prompts_dir = root_dir + "/prompts/"
    try:
        root = tk.Tk()
        root.title("Prompt Generator")
        root.configure(bg="#000000")  # Set root background to dark

        # Initialize FileSelector
        selector_frame = tk.Frame(root, bg="#000000")
        selector_frame.pack(fill=tk.BOTH, expand=True)
        selector = FileSelector(selector_frame, root_dir)

        # Initialize StaticRulesUI at the bottom
        rules_frame = tk.Frame(root, bg="#000000", padx=10, pady=10)
        rules_frame.pack(fill=tk.X, side=tk.BOTTOM)
        static_rules_ui = StaticRulesUI(rules_frame)

        root.mainloop()
        root.destroy()
    except Exception as e:
        print(f"[ERROR] Failed to initialize interface: {e}")
        return None

    selected_rules = static_rules_ui.get_selected_rules()

    if not selector.selected_files:
        print("[INFO] No files selected, exiting prompt generation.")
        return None

    prompt = "Here are the selected files and their contents:\n\n"
    for file_path in selector.selected_files:
        file_content = read_file_content(file_path)
        prompt += f"### File: {file_path}\n{file_content}\n\n"

    fs_generator = FileStructureGenerator(workspace_dir)
    file_structure = fs_generator.get_file_structure_string()
    prompt += "### Workspace File Structure:\n" + file_structure + "\n"

    if selector.user_input:
        prompt += f"### Additional Instructions:\n{selector.user_input}\n"

    # Append only selected static rules to the prompt
    prompt += f"### Selected Rules:\n" + "\n".join(selected_rules) + "\n"

    user_prompt_file = save_user_input(prompts_dir, selector.user_input)
    if user_prompt_file:
        print(f"user prompt saved to: {user_prompt_file}")
    else:
        print("[ERROR] Prompt could not be saved.")

    return prompt

def main():
    generate_full_prompt(r"C:\projects\portfoliomanager\prompt_generator\\")

if __name__ == "__main__":
    main()