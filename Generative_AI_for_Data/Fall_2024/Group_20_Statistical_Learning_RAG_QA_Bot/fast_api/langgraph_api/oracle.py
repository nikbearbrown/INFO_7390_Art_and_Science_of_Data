from langchain_core.agents import AgentAction
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from fast_api.langgraph_api.langgraph_tools import rag_search, fetch_arxiv, web_search, final_answer
from fast_api.langgraph_api.utilities import create_scratchpad
from fast_api.langgraph_api.config import OPENAI_API_KEY

system_prompt = """
You are the supervisor, the great AI tool manager. The user's query contains the input question along with index_name.
The format of query is: "Query, index_name: nameofindex".
The first tool you must use rag_search. Where you must send the query and index_name.

If relevant information is found in the rag_search tool then you must navigate 
to the web_search tool by sending the query to this tool. Upon returning from the web_search tool 
you must send the query to the fetch_arxiv tool to retrieve the content from relevant arxiv
pages. You are allowed to reuse tools to get additional information if necessary.

If you see that a tool has been used (in the scratchpad) with a particular
query, do NOT use that same tool with the same query again. Also, do NOT use
any tool more than twice (ie, if the tool appears in the scratchpad twice, do
not use it again).

You should aim to collect information from a diverse range of sources before
providing the answer to the user. Once you have collected plenty of information
to answer the user's question (stored in the scratchpad) use the final_answer
tool.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}, index_name: {index_name}"),
    ("assistant", "scratchpad: {scratchpad}"),
])

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)

tools=[
    rag_search,
    web_search,
    fetch_arxiv,
    final_answer
]

oracle = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "index_name": lambda x: x["index_name"],
        "scratchpad": lambda x: create_scratchpad(
            intermediate_steps=x["intermediate_steps"]
        ),
    }
    | prompt
    | llm.bind_tools(tools, tool_choice="any")
)

def run_oracle(state: list):

    state["resources"] = state.get("resources", [])
    state["logs"] = state.get("logs", [])

    print("run_oracle")
    print(f"intermediate_steps: {state['intermediate_steps']}")
    out = oracle.invoke(state)
    tool_name = out.tool_calls[0]["name"]
    tool_args = out.tool_calls[0]["args"]
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log="TBD"
    )

    return {
        "intermediate_steps": [action_out]
    }
    
tool_str_to_func = {
    "rag_search": rag_search,
    "fetch_arxiv": fetch_arxiv,
    "web_search": web_search,
    "final_answer": final_answer
}

def run_tool(state: list):
    # use this as helper function so we repeat less code
    tool_name = state["intermediate_steps"][-1].tool
    tool_args = state["intermediate_steps"][-1].tool_input
    print(f"{tool_name}.invoke(input={tool_args})")
    # run tool
    out = tool_str_to_func[tool_name].invoke(input=tool_args)
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log=str(out)
    )
    return {"intermediate_steps": [action_out]}