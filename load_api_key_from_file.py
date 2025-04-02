import json
from langchain.chat_models import ChatOpenAI

def load_api_key_from_file(path="OAI_CONFIG_LIST.json"):
    with open(path, "r") as f:
        config = json.load(f)

    api_key = config[0]["api_key"]
    return api_key;