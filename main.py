from typing import TypedDict, Literal
import random
from PIL import Image
from io import BytesIO

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from load_api_key_from_file import load_api_key_from_file

def main():
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

img_data = graph.get_graph().draw_mermaid_png()
img = Image.open(BytesIO(img_data))
img.show()

final_state = graph.invoke({"graph_state": "Hi, this is martijn"})
print(final_state)

if __name__ == "__main__":
    main()
