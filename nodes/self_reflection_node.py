import openai
from config import AppConfig
from TaskState import TaskState, Message
from pydantic import ValidationError

from state_logger import StateLogger


class SelfReflectionNode:
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
            print("Invalid state in SelfReflectionNode:", e)
            raise

        if not task_state.error:
            return state

        # Zoek eerste user-prompt in messages
        user_prompt = next(
            (m.content for m in task_state.messages if m.role == "user"),
            "<no user prompt found>"
        )

        file_structure = task_state.file_structure

        reflection_prompt = (
            f"The previous attempt to run the code resulted in an error:\n{task_state.error}\n\n"
            f"User prompt:\n{user_prompt}\n\n"
            f"Current project structure:\n{file_structure}\n\n"
            f"Please correct the code and return an updated list of files with their contents."
        )

        messages = [
            {"role": "system", "content": "You are a code reviewer. Improve faulty code based on the error message."},
            {"role": "user", "content": reflection_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2
        )

        content = response.choices[0].message.content
        task_state.messages.append(Message(role="reviser", content=content))
        task_state.error = None
        StateLogger.log_state(state, "SelfReflectionNode")
        return task_state.model_dump()
