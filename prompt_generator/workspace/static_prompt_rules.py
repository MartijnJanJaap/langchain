# filename: static_prompt_rules.py

def get_static_rules():
    rules = [
        "Always return full files because the code you output is automatically copied."
    ]
    return "\n".join(rules)

