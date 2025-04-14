import subprocess
import sys
import tempfile
from pathlib import Path

from config import AppConfig
from nodes.TaskState import TaskState, Message
from pydantic import ValidationError
from nodes.state_logger import StateLogger
import re

class ExecutorNode:
    def __init__(self, config: AppConfig):
        self.config = config

    def __call__(self, state):
        StateLogger.log_state(state, "ExecutorNode")
        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            StateLogger.log_msg("Invalid state in ExecutorNode", "ExecutorNode")
            raise

        # Vind de laatste gegenereerde code
        code_msg = next(
            (m.content for m in reversed(task_state.messages)
             if m.role in ("programmer", "reviser") and "```python" in m.content),
            None
        )

        if not code_msg:
            task_state.error = "No code block found in messages."
            return task_state.model_dump()

        # Extract code from markdown block
        match = re.search(r"```python\\n(.*?)```", code_msg, re.DOTALL)
        if not match:
            task_state.error = "Could not extract code from code block."
            return task_state.model_dump()

        code = match.group(1).strip()

        # Schrijf naar tijdelijk bestand in workspace
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", dir=self.config.workspace_path, delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                text=True
            )
            output = result.stdout.strip()
            error_output = result.stderr.strip()
            success = result.returncode == 0 and not error_output

            task_state.messages.append(
                Message(role="executor", content=output if success else error_output)
            )
            task_state.error = None if success else error_output

        except subprocess.TimeoutExpired as e:
            task_state.messages.append(Message(role="executor", content=f"Timeout: {str(e)}"))
            task_state.error = str(e)

        finally:
            Path(tmp_path).unlink(missing_ok=True)

        return task_state.model_dump()
