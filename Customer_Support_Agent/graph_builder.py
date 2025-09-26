# Build and Compile the Graph
from langgraph.graph import StateGraph,END
from langgraph.checkpoint.memory import MemorySaver
from agent_state import AgentState
from nodes import prompt_node,tool_node

def build_agent_graph()-> tuple:
    graph = StateGraph(AgentState)
    graph.add_node("Prompt",prompt_node)
    graph.add_node("Tools",tool_node)
    graph.add_edge("Prompt","Tools")
    graph.add_edge("Tools",END)
    graph.set_entry_point("Prompt")

    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)
    return app