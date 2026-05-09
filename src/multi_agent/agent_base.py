from __future__ import annotations

from multi_agent.constants import TOOL_LOOP_MAX
from multi_agent.llm.protocol import ChatClient, ChatResult
from multi_agent.prompts import system_prompt_for
from multi_agent.tools.registry import ToolContext, ToolRegistry
from multi_agent.types import AgentRole, Task


class BaseAgent:
    """Runs the standard tool-calling loop against an LLM."""

    def __init__(
        self,
        role: AgentRole,
        registry: ToolRegistry,
        llm: ChatClient,
    ) -> None:
        self.role = role
        self.registry = registry
        self.llm = llm

    def run(self, task: Task, ctx: ToolContext) -> str:
        system = system_prompt_for(self.role)
        messages: list[dict] = [
            {"role": "system", "content": system},
            {"role": "user", "content": task.description},
        ]
        tools = self.registry.openai_tools_payload()

        for _ in range(TOOL_LOOP_MAX):
            result = self.llm.chat(messages, tools)
            if not result.tool_calls:
                return (result.content or "").strip()
            assistant_payload = self._assistant_message(result)
            messages.append(assistant_payload)
            for tc in result.tool_calls:
                tool_output = self.registry.execute(tc.name, tc.arguments, ctx)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_output,
                    }
                )

        return "error: tool loop limit exceeded"

    @staticmethod
    def _assistant_message(result: ChatResult) -> dict:
        payload: dict = {
            "role": "assistant",
            "content": result.content or "",
        }
        if result.tool_calls:
            payload["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": tc.arguments},
                }
                for tc in result.tool_calls
            ]
        return payload
