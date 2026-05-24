import pytest

from multi_agent.memory import SharedMemory
from multi_agent.tools.file_tools import file_tool_definitions
from multi_agent.tools.registry import ToolContext, ToolRegistry


def _ctx(tmp_path):
    return ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))


def test_read_text_file_utf8(tmp_path):
    (tmp_path / "hello.txt").write_text("hola", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("read_text_file", '{"path": "hello.txt"}', _ctx(tmp_path))
    assert out == "hola"



def test_read_text_file_rejects_traversal(tmp_path):
    reg = ToolRegistry(file_tool_definitions())
    with pytest.raises(ValueError, match="path escapes"):
        reg.execute("read_text_file", '{"path": "../etc/passwd"}', _ctx(tmp_path))


def test_read_text_file_rejects_binary(tmp_path):
    (tmp_path / "bin.dat").write_bytes(b"\x00\x01\x02")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("read_text_file", '{"path": "bin.dat"}', _ctx(tmp_path))
    assert "binary" in out

