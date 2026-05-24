from multi_agent.delegation import DelegationRouter
from multi_agent.types import AgentRole


def test_delegation_weighted_scoring():
    router = DelegationRouter()
    role = router.route("please refactor the implementation")
    assert role == AgentRole.CODING


def test_delegation_reviewer_wins_tie():
    router = DelegationRouter(
        keywords={
            AgentRole.WRITER: ("write",),
            AgentRole.REVIEWER: ("write",),
            AgentRole.PLANNER: ("x",),
        }
    )
    assert router.route("write") == AgentRole.REVIEWER


def test_delegation_custom_default():
    router = DelegationRouter(
        keywords={AgentRole.DATA: ("metric",)},
        default_role=AgentRole.DATA,
    )
    assert router.route("hello") == AgentRole.DATA
    assert router.route("show metric") == AgentRole.DATA

