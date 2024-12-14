from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage

from langchain_core.agents import AgentAction
import operator

class AgentState(TypedDict):
    input: str
    index_name: str
    chat_history: list[BaseMessage]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]