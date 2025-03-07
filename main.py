import autogen

def main():
    config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json"
    )

    with open("workspace/reports/csv/stock_report_2025-03-05.csv", "r") as f:
        stock_report = f.read()

    with open("workspace/csv_report_viewer.html", "r") as f:
        existing_html_code = f.read()

    with open("workspace/generate_html.py", "r") as f:
        generate_html_code = f.read()

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={
            "config_list": config_list
        }
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="TERMINATE",
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False
        },
        max_consecutive_auto_reply=4
    )

    user_proxy.initiate_chat(
        assistant,
        message= "have a look for the part of the csv report  " + stock_report
                 + "I want a standalone html/js page that acts as a front for the stock report."
                   "I want to be able to sort filter all columns. You should use python to generate a html page."
                   "this is the generated html code " + existing_html_code +
                 " this is the code that generate html files " + generate_html_code+
                 " I want you to update the generate html file code to have a search input bar where i can search/filter all columns and rows"

    )

if __name__ == "__main__":
    main()