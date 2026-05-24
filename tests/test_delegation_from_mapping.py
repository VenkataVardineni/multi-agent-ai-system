from multi_agent.delegation import DelegationRouter
from multi_agent.types import AgentRole


def test_from_mapping_custom_keywords():
    router = DelegationRouter.from_mapping({"data": ("metric", "csv")})
    assert router.route("show metric trends") == AgentRole.DATA

