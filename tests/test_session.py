from multi_agent.memory import SharedMemory
from multi_agent.session import AgentSession
from multi_agent.tools import build_default_registry


def test_agent_session_metadata():
    session = AgentSession(
        memory=SharedMemory(),
        registry=build_default_registry(),
        metadata={"run_id": "abc"},
    )
    assert session.metadata["run_id"] == "abc"

