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
        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            StateLogger.log_msg("Invalid state in ExecutorNode", "ExecutorNode")
            raise

        task_state.error = None
        error_messages = []

        code_msg = next(
            (m.content for m in reversed(task_state.messages)
             if m.role in ("programmer", "reviser") and "```python" in m.content),
            None
        )

        if not code_msg:
            error_messages.append("No code block found in messages.")
        else:
            match = re.search(r"```python\n(.*?)```", code_msg, re.DOTALL)
            if not match:
                error_messages.append("Could not extract code from code block.")
            else:
                code = match.group(1).strip()

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

                    visible_output = output if success else error_output

                    formatted_output = (
                        "\n========== OUTPUT ExecutorNode =========="
                        f"\n{visible_output or '<no output>'}\n"
                        "========================================\n"
                    )

                    task_state.messages.append(
                        Message(role="executor", content=formatted_output)
                    )
                    if not success or "error" in visible_output.lower():
                        error_messages.append(error_output or visible_output)

                except subprocess.TimeoutExpired as e:
                    error_msg = f"Timeout: {str(e)}"
                    task_state.messages.append(Message(role="executor", content=error_msg))
                    error_messages.append(error_msg)

                finally:
                    Path(tmp_path).unlink(missing_ok=True)

        if error_messages:
            task_state.error = "\n".join(error_messages)

        StateLogger.log_state(task_state, "ExecutorNode")
        return task_state.model_dump()
