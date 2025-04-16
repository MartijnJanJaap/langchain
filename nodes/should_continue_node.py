from TaskState import TaskState
from pydantic import ValidationError
from state_logger import StateLogger
from openai import OpenAI
from config import AppConfig
from pathlib import Path

class ShouldContinueNode:
    def __init__(self, config: AppConfig, max_iterations=2):
        self.max_iterations = max_iterations
        self.client = OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url
        )
        self.model = config.llm_model
        self.prompts_dir = config.prompts_dir

    def __call__(self, state):
        StateLogger.log_state(state, "ShouldContinueNode")
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

        if task_state.error is None:
            user_input = self.get_last_prompt_text()
            last_executor_output = next(
                (m.content for m in reversed(task_state.messages) if m.role == "executor"),
                ""
            )

            prompt = (
                "You are a smart decision-making agent.\n"
                "Based on the user's original request and the final code output, determine if the task was completed successfully. The goal is more important then the code.\n"
                "Reply only with one of the following: SUCCESS, FAILURE, or NOT_SURE."
                "in newline give detailed reason why you chose that. \n\n"
                f"User request:\n{user_input}\n\nCode output:\n{last_executor_output}\n"
            )

            print("\n========== PROMPT TO LLM (ShouldContinueNode) ==========")
            print(prompt)
            print("=======================================================\n")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You evaluate results of programming tasks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            decision = response.choices[0].message.content.strip().upper()

            print("========== OUTPUT ShouldContinueNode ==========")
            print(f"LLM Decision: {decision}")
            print("===============================================\n")

            if "SUCCESS" in decision:
                task_state.should_continue = False
            elif "FAILURE" in decision:
                task_state.should_continue = True
            else:
                task_state.should_continue = False

        else:
            task_state.should_continue = attempts < self.max_iterations

        if not task_state.should_continue:
            print("[ShouldContinueNode] Asking user for next instruction.")
        else:
            print("[ShouldContinueNode] Continuing automatically.")

        return task_state.model_dump()

    def get_last_prompt_text(self):
        if not self.prompts_dir.exists():
            return ""

        prompt_files = sorted(self.prompts_dir.glob("prompt_*.txt"), reverse=True)
        if not prompt_files:
            return ""

        return prompt_files[0].read_text().strip()
