import openai
from config import AppConfig

class SelfReflectionNode:
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url
        )
        self.model = config.llm_model

    def __call__(self, state):
        error = state.get("error")
        if not error:
            return state

        user_prompt = state["messages"][0]["content"]
        file_structure = state["file_structure"]

        reflection_prompt = (
            f"The previous attempt to run the code resulted in an error:\n{error}\n\n"
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
        messages_log = state.get("messages", [])
        messages_log.append({"role": "reviser", "content": content})

        return {
            **state,
            "messages": messages_log,
            "error": None
        }
