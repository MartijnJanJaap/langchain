from nodes.TaskState import TaskState
from pydantic import ValidationError

class ShouldContinueNode:
    def __init__(self, max_iterations=5):
        self.max_iterations = max_iterations

    def __call__(self, state):
        print(str(state))
        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            print("Invalid state in ShouldContinueNode:", e)
            raise

        attempts = len([
            m for m in task_state.messages
            if m.role in ("programmer", "reviser")
        ])

        print(f"[ShouldContinueNode] Attempt count: {attempts}")

        task_state.should_continue = attempts < self.max_iterations

        if not task_state.should_continue:
            print("[ShouldContinueNode] Maximum attempts reached. Asking user for next instruction.")
        else:
            print("[ShouldContinueNode] Continuing automatically.")

        return task_state.model_dump()
