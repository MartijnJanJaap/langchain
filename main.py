from typing import TypedDict, Literal
import random
from PIL import Image
from io import BytesIO

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from load_api_key_from_file import load_api_key_from_file

api_key = load_api_key_from_file()


class State(TypedDict):
    graph_state: str

def node_1(state):
    print(" node 1 ")
    return {"graph_state": state["graph_state"] + " I am"}

def node_2(state):
    print(" node 2 ")
    return {"graph_state": state["graph_state"] + " happy!"}

def node_3(state):
    print(" node 3 ")
    return {"graph_state": state["graph_state"] + " sad."}

def decide_mood(state) -> Literal["node_2", "node_3"]:

    user_input = state["graph_state"]
    if random.random() < 0.5:
        return "node_2"
    return "node_3"

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

# visualize:
# img_data = graph.get_graph().draw_mermaid_png()
# img = Image.open(BytesIO(img_data))
# img.show()

final_state = graph.invoke({"graph_state": "Hi, this is martijn"})
print(final_state)





from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

messages = [AIMessage(content=f"So you said you were researching ocean mammals?", name="Model")]
messages.extend([HumanMessage(content=f"Yes thats right.", name="Martijn")])
messages.extend([AIMessage(content=f"Great, what would you like to learn about them?.", name="Model")])
messages.extend([HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Martijn")])

for m in messages:
    m.pretty_print()



from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model = "gpt-4o", api_key= api_key)
result = llm.invoke(messages)
print(type(result))
print(result)



def multiply(a: int, b: int) -> int:
    """Multiply a nd b.

    Args:
     a: first int
    b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])
tool_call = llm_with_tools.invoke([HumanMessage(content = f" what is 3 multiplied by 20 ", name="Martijn")])
print(tool_call)