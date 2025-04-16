from pathlib import Path
from langgraph.graph import StateGraph, END
import json

from nodes.TaskState import TaskState, Message
from nodes.user_proxy_node import UserProxyNode
from nodes.code_generator_node import CodeGeneratorNode
from nodes.executor_node import ExecutorNode
from nodes.self_reflection_node import SelfReflectionNode
from nodes.should_continue_node import ShouldContinueNode

from config import AppConfig


def should_reflect(state):
    return "reflect" if "error" in state and bool(state["error"]) else "decide"

def should_continue(state):
    return "generate" if state.get("should_continue", False) else "user"


class GraphBuilder:
    def __init__(self, config: AppConfig):
        self.config = config

    def build_graph(self):
        user_node = UserProxyNode(self.config)
        code_gen_node = CodeGeneratorNode(self.config)
        executor_node = ExecutorNode(self.config)
        reflection_node = SelfReflectionNode(self.config)
        continue_node = ShouldContinueNode(self.config)

        builder = StateGraph(dict)

        builder.add_node("user", user_node)
        builder.add_node("generate", code_gen_node)
        builder.add_node("execute", executor_node)
        builder.add_node("reflect", reflection_node)
        builder.add_node("decide", continue_node)

        builder.set_entry_point("user")

        builder.add_edge("user", "generate")
        builder.add_edge("generate", "execute")
        builder.add_conditional_edges("execute", should_reflect, {
            "reflect": "reflect",
            "decide": "decide"
        })
        builder.add_edge("reflect", "decide")
        builder.add_conditional_edges("decide", should_continue, {
            "generate": "generate",
            "user": "user"
        })

        builder.set_finish_point("user")

        return builder.compile()


if __name__ == "__main__":
    with open("../OAI_CONFIG_LIST.json") as f:
        llm_config_file = json.load(f)

    config = AppConfig(
        workspace_path=Path("workspace"),
        prompts_dir=Path("prompts"),
        llm_model=llm_config_file[0]["model"],
        llm_api_key=llm_config_file[0]["api_key"],
        llm_base_url=llm_config_file[0].get("base_url")
    )

    # Use Pydantic state object and convert to dict
    initial_state = TaskState(
        messages=[Message(role="user", content="")],
        file_structure="",
        error=None,
        should_continue=False
    ).model_dump()

    graph = GraphBuilder(config).build_graph()
    graph.invoke(initial_state)

