# filename: auto_select_files_based_on_prompt.py
import os
import json

# Assuming OpenAI class is correctly implemented and available
from openai import OpenAI

from prompt_generator.workspace.file_structure_generator import FileStructureGenerator

class OpenAIIntegration:

    @staticmethod
    def get_files_which_are_related_to_prompt(prompt, root_dir):
        try:

            print("\n\n this is the prompt: {}".format(prompt))

            config_path = os.path.abspath(os.path.join(__file__, "../../../OAI_CONFIG_LIST.json"))
            api_key = get_api_key_from_config(config_path)
            client = OpenAI(api_key=api_key)

            fs_generator = FileStructureGenerator(root_dir)
            file_structure = fs_generator.get_file_structure_string()
            prompt += " " + file_structure

            prompt += (
                "\nAbove are the file structure and prompt.\n"

                "Based on the provided file structure, please list the file paths, everything after /workspace, you believe are most relevant. which file need a change? the fever the better."
                "in relation to interacting with the prompt described. Only provide the list of paths without explanatory text. max 3."
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            response_content = response.choices[0].message.content.strip()
            path_lines = [line.strip() for line in response_content.splitlines() if line.strip()]

            # Remove any leading characters such as '- ' from each line
            cleaned_paths = [path.lstrip("- ").strip() for path in path_lines]
            # Convert relative paths to absolute paths
            absolute_paths = [os.path.join(root_dir, path.strip('/')) for path in cleaned_paths]
            return absolute_paths
        except Exception as e:
            print(f"[ERROR] Failed to call OpenAI API: {e}")
            return []

def get_api_key_from_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config[0].get('api_key')
    except Exception as e:
        print(f"[ERROR] Failed to read API key from config: {e}")
        return None

# Example usage
if __name__ == "__main__":
    root_dir = "C:\\projects\\git\\portfoliomanager\\prompt_generator\\workspace"
    prompt = "I want to extract auto select functionality more into methods in the same file"

    absolute_related_files = OpenAIIntegration().get_files_which_are_related_to_prompt(prompt, root_dir)
    print("Related absolute file paths:\n", "\n".join(absolute_related_files))