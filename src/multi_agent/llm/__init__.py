"""LLM clients used by agents."""

from multi_agent.llm.mock import MockLLM
from multi_agent.llm.openai_client import OpenAICompatClient
from multi_agent.llm.protocol import ChatClient, ChatResult, ToolCallSpec

__all__ = [
    "ChatClient",
    "ChatResult",
    "ToolCallSpec",
    "MockLLM",
    "OpenAICompatClient",
]
