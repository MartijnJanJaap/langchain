import subprocess
import sys
from config import AppConfig

class ExecutorNode:
    def __init__(self, config: AppConfig, entry_file="main.py"):
        self.config = config
        self.entry_file = entry_file

    def __call__(self, state):
        workspace = self.config.workspace_path
        entry_path = workspace / self.entry_file

        if not entry_path.exists():
            return {
                **state,
                "error": f"Cannot find {self.entry_file} in {workspace}"
            }

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
            error = result.stderr.strip()
            success = result.returncode == 0 and not error

            messages = state.get("messages", [])
            messages.append({
                "role": "executor",
                "content": output if success else error
            })

            return {
                **state,
                "messages": messages,
                "error": None if success else error
            }

        except subprocess.TimeoutExpired as e:
            error = f"Timeout while running {self.entry_file}: {str(e)}"
            messages = state.get("messages", [])
            messages.append({"role": "executor", "content": error})

            return {
                **state,
                "messages": messages,
                "error": error
            }