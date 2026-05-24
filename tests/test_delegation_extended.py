from multi_agent.delegation import DelegationRouter
from multi_agent.types import AgentRole


def test_delegation_weighted_scoring():
    router = DelegationRouter()
    role = router.route("please refactor the implementation")
    assert role == AgentRole.CODING

