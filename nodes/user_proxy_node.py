from datetime import datetime
from pydantic import ValidationError

from nodes.TaskState import TaskState, Message
from nodes.file_structure_generator import FileStructureGenerator
from config import AppConfig
from nodes.state_logger import StateLogger


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
        self.config.prompts_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.config.prompts_dir / f"prompt_{timestamp}.txt"
        filename.write_text(prompt_text)

        task_state.messages.append(Message(role="user", content=prompt_text))
        task_state.file_structure = FileStructureGenerator.get_file_structure_string(self.config.workspace_path)
        task_state.error = None
        task_state.should_continue = False

        return task_state.model_dump()

    def get_user_input(self):
        print("Enter your prompt:")
        return input().strip()
