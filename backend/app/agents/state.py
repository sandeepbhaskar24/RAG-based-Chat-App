from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AnyMessage, BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    question: str
    history: list[BaseMessage]
    has_docs: bool
    route: Literal["direct", "retrieve", "weather"]

    # KB planning fields
    task_type: Literal["simple", "document_summary", "complex"]
    retrieval_strategy: Literal["single_search", "multi_search", "full_document"]
    needs_verification: bool

    messages: Annotated[list[AnyMessage], add_messages]
    steps: int
