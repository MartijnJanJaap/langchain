from datetime import datetime

from nodes.file_structure_generator import FileStructureGenerator
from config import AppConfig


class UserProxyNode:
    def __init__(self, config: AppConfig):
        self.config = config

    def __call__(self, state):
        prompt_text = self.get_user_input()
        self.config.prompts_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.config.prompts_dir / f"prompt_{timestamp}.txt"
        filename.write_text(prompt_text)

        file_structure = FileStructureGenerator.get_file_structure_string(self.config.workspace_path)

        messages = state.get("messages", [])
        messages.append({"role": "user", "content": prompt_text})

        return {
            **state,
            "messages": messages,
            "file_structure": file_structure,
            "error": None,
            "should_continue": False
        }

    def get_user_input(self):
        print("Enter your prompt:")
        return input().strip()
