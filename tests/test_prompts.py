from multi_agent.prompts import system_prompt_for
from multi_agent.types import AgentRole


def test_system_prompt_for_planner():
    prompt = system_prompt_for(AgentRole.PLANNER)
    assert "Planner" in prompt

