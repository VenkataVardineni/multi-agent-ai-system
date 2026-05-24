import pytest

from multi_agent.types import Message


def test_message_is_frozen():
    msg = Message(role="user", content="hi")
    with pytest.raises(Exception):
        msg.content = "changed"

