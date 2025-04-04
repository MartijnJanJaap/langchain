import os
import re
import subprocess
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from load_api_key_from_file import load_api_key_from_file

api_key = load_api_key_from_file()
llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=api_key)

# Constants
WORKDIR = "./workspace"
MAX_RETRIES = 3
os.makedirs(WORKDIR, exist_ok=True)

# Define typed state
class CodeState(TypedDict):
    task: str
    context: str
    code: str
    code_path: str
    output: str
    error: str
    attempt: int

# 1. Task input node (initializes attempt/context if not set)
def task_input_node(state: CodeState) -> CodeState:
    return {
        **state,
        "context": state.get("context", ""),
        "attempt": 0
    }

# 2. Code generation node
def code_gen_node(state: CodeState) -> CodeState:
    prompt = f"Schrijf alleen de uitvoerbare Python-code voor de volgende taak:\n{state['task']}\n\n{state['context']}"
    response = llm.invoke(prompt)
    return {
        **state,
        "code": response.content
    }

# 3. Save code node (extracts code blocks if needed)
def code_save_node(state: CodeState) -> CodeState:
    code = state["code"]
    match = re.search(r"```(?:python)?\n(.*?)```", code, re.DOTALL)
    clean_code = match.group(1).strip() if match else code.strip()

    filename = os.path.join(WORKDIR, "code.py")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean_code)
    return {
        **state,
        "code_path": filename
    }

# 4. Execute code node
def code_exec_node(state: CodeState) -> CodeState:
    try:
        result = subprocess.run(["python", state["code_path"]], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {
                **state,
                "output": result.stdout,
                "error": result.stderr
            }
        return {
            **state,
            "output": result.stdout,
            "error": ""
        }
    except Exception as e:
        return {
            **state,
            "output": "",
            "error": str(e)
        }

# 5. Error check node
def error_check_node(state: CodeState) -> str:
    if state["error"] and state["attempt"] < MAX_RETRIES:
        return "retry"
    elif state["error"]:
        return "abort"
    else:
        return "success"

# 6. Retry handler
def retry_node(state: CodeState) -> CodeState:
    return {
        **state,
        "attempt": state["attempt"] + 1,
        "context": f"De vorige code gaf deze fout:\n{state['error']}\nProbeer opnieuw. Geef alleen uitvoerbare Python-code terug."
    }

# 7. Abort node
def abort_node(state: CodeState) -> CodeState:
    print("Code generatie mislukt na meerdere pogingen.")
    print("Laatste fout:", state["error"])
    return state

# 8. Success node
def success_node(state: CodeState) -> CodeState:
    print("Code succesvol uitgevoerd. Output:")
    print(state["output"])
    return state

# Graph opbouwen
builder = StateGraph(CodeState)
builder.add_node("task_input", task_input_node)
builder.add_node("code_gen", code_gen_node)
builder.add_node("code_save", code_save_node)
builder.add_node("code_exec", code_exec_node)
builder.add_node("retry_handler", retry_node)
builder.add_node("abort", abort_node)
builder.add_node("success", success_node)
builder.add_conditional_edges("code_exec", error_check_node, {
    "retry": "retry_handler",
    "abort": "abort",
    "success": "success"
})
builder.add_edge("task_input", "code_gen")
builder.add_edge("retry_handler", "code_gen")
builder.add_edge("code_gen", "code_save")
builder.add_edge("code_save", "code_exec")
builder.set_entry_point("task_input")
builder.set_finish_point("success")

graph = builder.compile()

# Run
if __name__ == "__main__":
    graph.invoke({
        "task": "Print de eerste 5 even getallen met een for-loop.",
        "context": "",
        "code": "",
        "code_path": "",
        "output": "",
        "error": "",
        "attempt": 0
    })