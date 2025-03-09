import os


def get_last_known_prompt(prompts_dir):
    try:
        if not os.path.exists(prompts_dir):
            print("No prompts directory exists")
            return ""

        prompt_files = [os.path.join(prompts_dir, f) for f in os.listdir(prompts_dir) if f.endswith(".txt")]
        if not prompt_files:
            return ""

        latest_prompt_file = max(prompt_files, key=os.path.getctime)

        with open(latest_prompt_file, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        print(f"[ERROR] Failed to retrieve last known prompt: {e}")
        return ""