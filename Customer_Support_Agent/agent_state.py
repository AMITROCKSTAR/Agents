#Define the Agent State
from typing import Annotated, TypedDict, List
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage],"Conversation History"]
    query: str
    result: str
    selected_tool:str
    tool_reason:str