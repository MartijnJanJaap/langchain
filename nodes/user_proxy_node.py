from datetime import datetime
from pydantic import ValidationError

from TaskState import TaskState, Message
from file_structure_generator import FileStructureGenerator
from config import AppConfig
from state_logger import StateLogger


class UserProxyNode:
    def __init__(self, config: AppConfig):
        self.config = config

    def __call__(self, state):
        StateLogger.log_state(state, "UserProxyNode")

        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            StateLogger.log_msg("Invalid state", "UserProxyNode")
            raise

        prompt_text = self.get_user_input()
        if prompt_text.strip().lower() == "exit":
            print("\n[UserProxyNode] Exit command received. Shutting down gracefully.")
            exit(0)

        self.save_prompt_if_applicable(prompt_text, task_state)

        task_state.messages.append(Message(role="user", content=prompt_text))
        task_state.file_structure = FileStructureGenerator.get_file_structure_string(self.config.workspace_path)
        task_state.error = None
        task_state.should_continue = False

        return task_state.model_dump()

    def save_prompt_if_applicable(self, prompt_text, task_state):
        already_has_user_prompt = any(m.role == "user" for m in task_state.messages)
        if not already_has_user_prompt:
            self.config.prompts_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.config.prompts_dir / f"prompt_{timestamp}.txt"
            filename.write_text(prompt_text)

    def get_user_input(self):
        print("User input required. 'exit' to stop the script. Enter your prompt:")
        return input().strip()
