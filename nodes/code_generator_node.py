import openai
from pathlib import Path
from config import AppConfig

class CodeGeneratorNode:
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url
        )
        self.model = config.llm_model

    def __call__(self, state):
        system_prompt = (
            "You are a programming assistant. Use the user's prompt and project structure below "
            "to generate code. Output a list of absolute file paths and their contents in the format:\n\n"
            "/absolute/path/to/file.py\n```python\n...code...\n```"
        )

        user_prompt = state["messages"][-1]["content"]
        file_structure = state["file_structure"]
        prompt = f"User prompt:\n{user_prompt}\n\nProject structure:\n{file_structure}\n"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content
        generated_files = self.parse_files_from_response(content, self.config.workspace_path)

        messages_log = state.get("messages", [])
        messages_log.append({"role": "programmer", "content": content})

        return {
            **state,
            "messages": messages_log,
            "error": None
        }

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
