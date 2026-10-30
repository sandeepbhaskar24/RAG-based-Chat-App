from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AnyMessage, BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    question: str
    history: list[BaseMessage]                     # prior chat turns (token-budgeted)
    has_docs: bool                                 # does the user have any indexed document?
    route: Literal["direct", "retrieve", "weather"]
    messages: Annotated[list[AnyMessage], add_messages]   # agent scratchpad (tool calls/results)
    steps: int                                     # agent turns so far (loop guard)