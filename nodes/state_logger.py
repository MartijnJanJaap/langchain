import json
from pydantic import BaseModel

class StateLogger:
    @staticmethod
    def log_state(state: BaseModel | dict, node: str = ""):
        print(f"\n--- STATE in [{node}] ---")

        messages = []
        if isinstance(state, BaseModel):
            state_dict = state.model_dump()
        else:
            state_dict = state

        # Extract last message (if any)
        messages = state_dict.get("messages", [])
        if messages:
            last_msg = messages[-1]
            print(f"Last message [{last_msg['role']}]: {last_msg['content']}")
        else:
            print("(no messages)")

        print(f"Error: {state_dict.get('error')}")
        print(f"Should continue: {state_dict.get('should_continue')}")
        print(f"File structure: {state_dict.get('file_structure', '').strip() or '(empty)'}")

        print("-" * (22 + len(node)))

    @staticmethod
    def log_msg(msg: str, node: str = ""):
        prefix = f"[{node}] " if node else ""
        print(f"{prefix}{msg}")
