You will need a file in the root directory called OAI_CONFIG_LIST.json
With the following config:

````
[
  {
    "model": "gpt-4o", (or any model)
    "api_key": "openai_secret_key"
  }
]
````

pip install autogen
pip install ag2[openai]