from multi_agent.delegation import DelegationRouter
from multi_agent.types import AgentRole


def test_routes_to_planner_by_default():
    router = DelegationRouter()
    assert router.route("hello world") == AgentRole.PLANNER


def test_routes_keywords():
    router = DelegationRouter()
    assert router.route("please critique the narrative") == AgentRole.REVIEWER
    assert router.route("implement this patch for the API") == AgentRole.CODING
    assert router.route("analyze the csv columns") == AgentRole.DATA
