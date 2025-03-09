# filename: promptgenerator.py
import os
import tkinter as tk

from prompt_generator.workspace.file_selector import FileSelector
from prompt_generator.workspace.file_structure_generator import FileStructureGenerator
from prompt_generator.workspace.prompt_file_manager import save_user_input
from prompt_generator.workspace.read_file_content import read_file_content

def generate_full_prompt(workspace_dir, prompts_dir):
    try:
        root = tk.Tk()
        selector = FileSelector(root, workspace_dir, prompts_dir)

        root.mainloop()
        root.destroy()  # Ensure the Tkinter application is properly closed
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

    fs_generator = FileStructureGenerator(workspace_dir)
    file_structure = fs_generator.get_file_structure_string()
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