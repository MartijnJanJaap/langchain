import subprocess
import sys
from config import AppConfig
from nodes.TaskState import TaskState, Message
from pydantic import ValidationError

class ExecutorNode:
    def __init__(self, config: AppConfig, entry_file="main.py"):
        self.config = config
        self.entry_file = entry_file

    def __call__(self, state):
        print(str(state))
        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            print("Invalid state in ExecutorNode:", e)
            raise

        workspace = self.config.workspace_path
        entry_path = workspace / self.entry_file

        if not entry_path.exists():
            task_state.error = f"Cannot find {self.entry_file} in {workspace}"
            return task_state.model_dump()

        try:
            result = subprocess.run(
                [sys.executable, str(entry_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                text=True,
                cwd=str(workspace)
            )
            output = result.stdout.strip()
            error_output = result.stderr.strip()
            success = result.returncode == 0 and not error_output

            task_state.messages.append(
                Message(role="executor", content=output if success else error_output)
            )
            task_state.error = None if success else error_output

            return task_state.model_dump()

        except subprocess.TimeoutExpired as e:
            error_msg = f"Timeout while running {self.entry_file}: {str(e)}"
            task_state.messages.append(Message(role="executor", content=error_msg))
            task_state.error = error_msg

            return task_state.model_dump()
