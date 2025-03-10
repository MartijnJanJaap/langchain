import autogen
from prompt_generator.workspace import promptgenerator


def main():
    full_prompt = promptgenerator.generate_full_prompt("C:\projects\portfoliomanager\prompt_generator\\")

    if not full_prompt:
        print("No prompt generated.")
        return

    config_list = autogen.config_list_from_json(env_or_file="../OAI_CONFIG_LIST.json")

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={"config_list": config_list}
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="TERMINATE",
        code_execution_config={"work_dir": "workspace", "use_docker": False},
        max_consecutive_auto_reply=1
    )

    user_proxy.initiate_chat(assistant, message=full_prompt)

if __name__ == "__main__":
    main()
