from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class TaskState(BaseModel):
    messages: List[Message] = []
    file_structure: str = ""
    error: Optional[str] = None
    should_continue: bool = False

    def log(self, title: str = "TaskState") -> None:
        print(f"\n===== {title} =====")
        print(f"Should continue: {self.should_continue}")
        print(f"Error: {self.error}")
        print("Messages:")
        for i, msg in enumerate(self.messages):
            print(f"  [{i}] {msg.role}: {msg.content[:80]}{'...' if len(msg.content) > 80 else ''}")
        print("File structure:")
        print(self.file_structure.strip() or "(empty)")
        print("=" * (10 + len(title)))