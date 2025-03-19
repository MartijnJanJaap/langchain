# filename: save_prompt_input.py
import os
from datetime import datetime

def save_user_input(prompts_dir, prompt_text):
    try:
        os.makedirs(prompts_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(prompts_dir, f"{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to save prompt: {e}")
        return None