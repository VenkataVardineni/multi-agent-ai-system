from multi_agent.agent_base import BaseAgent
from multi_agent.llm.protocol import ChatClient
from multi_agent.tools.registry import ToolRegistry
from multi_agent.types import AgentRole


def build_writer_agent(registry: ToolRegistry, llm: ChatClient) -> BaseAgent:
    return BaseAgent(AgentRole.WRITER, registry, llm)
