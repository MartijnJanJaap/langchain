from io import BytesIO

from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from PIL import Image
from io import BytesIO

from load_api_key_from_file import load_api_key_from_file

api_key = load_api_key_from_file()

class State(MessagesState):
    pass

def multiply(a: int, b: int) -> int:
    """Multiply a nd b.

    Args:
     a: first int
    b: second int
    """
    return a * b

llm = ChatOpenAI(model = "gpt-4o", api_key= api_key)
llm_with_tools = llm.bind_tools([multiply])

def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

img_data = graph.get_graph().draw_mermaid_png()
img = Image.open(BytesIO(img_data))
img.show()

messages = graph.invoke({"messages": [HumanMessage(content="Hello!")]})
print(messages)