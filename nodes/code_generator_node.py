import openai
from pathlib import Path
from config import AppConfig
from nodes.TaskState import TaskState, Message
from pydantic import ValidationError

from nodes.state_logger import StateLogger


class CodeGeneratorNode:
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url
        )
        self.model = config.llm_model

    def __call__(self, state):
        try:
            task_state = TaskState.model_validate(state)
        except ValidationError as e:
            print("Invalid state:", e)
            raise

        last_user_message = next(
            (m.content for m in reversed(task_state.messages) if m.role == "user"), ""
        )
        if not last_user_message:
            raise ValueError("No user message found in state.")

        file_structure = task_state.file_structure

        system_prompt = (
            "You are a programming assistant. Use the user's prompt and project structure below "
            "You are not allowed to give additional instructions or any documentation."
            "I prefer code that doesn't need an api key."
            "to generate code. Output a list of absolute file paths and their contents in the format:\n\n"
            "/absolute/path/to/file.py\n```python\n...code...\n```"
        )

        prompt = f"User prompt:\n{last_user_message}\n\nProject structure:\n{file_structure}\n"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        print("\n========== PROMPT TO LLM (CodeGeneratorNode) ==========")
        print(prompt)
        print("======================================================\n")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content

        print("========== RESPONSE FROM LLM (CodeGeneratorNode) ==========")
        print(content)
        print("===========================================================\n")

        self.parse_files_from_response(content, self.config.workspace_path)

        task_state.messages.append(Message(role="programmer", content=content))
        task_state.error = None

        return task_state.model_dump()

    def parse_files_from_response(self, text, base_path):
        lines = text.splitlines()
        current_path = None
        buffer = []
        files = {}

        for line in lines:
            if line.startswith("/"):
                if current_path and buffer:
                    files[current_path] = "\n".join(buffer).strip("`\n")
                    buffer = []
                current_path = Path(line.strip())
            elif line.strip().startswith("```"):
                continue
            elif current_path:
                buffer.append(line)

        if current_path and buffer:
            files[current_path] = "\n".join(buffer).strip("`\n")

        for path, content in files.items():
            full_path = base_path / path.relative_to("/")
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        return list(files.keys())
