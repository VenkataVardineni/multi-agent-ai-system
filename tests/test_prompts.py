from multi_agent.prompts import system_prompt_for
from multi_agent.types import AgentRole


def test_system_prompt_for_planner():
    prompt = system_prompt_for(AgentRole.PLANNER)
    assert "Planner" in prompt

from multi_agent.prompts import SYSTEM_PROMPTS
from multi_agent.types import AgentRole


def test_all_roles_have_prompts():
    for role in AgentRole:
        assert role in SYSTEM_PROMPTS
        assert len(SYSTEM_PROMPTS[role]) > 20

