from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from fast_api.langgraph_api.oracle import run_tool, run_oracle
from fast_api.langgraph_api.state_schema import AgentState

graph = StateGraph(AgentState)

graph.add_node("oracle", run_oracle)
graph.add_node("rag_search", run_tool)
graph.add_node("fetch_arxiv", run_tool)
graph.add_node("web_search", run_tool)
graph.add_node("final_answer", run_tool)


def router(state: list):
    """Route after the oracle node."""
    
    if isinstance(state["intermediate_steps"], list):
        return state["intermediate_steps"][-1].tool
    else:
        print("Router invalid format")
        return "final_answer"


def rag_router(state: list):
    """Route after the rag_search node."""
    
    if state["intermediate_steps"][-1].log != "I don't know.":
        return "oracle"
    
    return END

graph.set_entry_point("oracle")
graph.add_conditional_edges(
    "oracle",
    router,
    ["rag_search", "web_search", "fetch_arxiv", "final_answer", END]
)
graph.add_conditional_edges(
    "rag_search",
    rag_router,
    ["oracle", END]
)
graph.add_edge("web_search", "oracle")
graph.add_edge("fetch_arxiv", "oracle")
graph.add_edge("final_answer", END)
runnable = graph.compile()

# out = runnable.invoke({
#     "input": "tell me something interesting about hedging for canadian investors",
#     "chat_history": [],
# })

# print(build_report(
#     output=out["intermediate_steps"][-1].tool_input
# ))
