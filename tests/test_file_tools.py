import json

import pytest

from multi_agent.exceptions import ToolExecutionError
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
    with pytest.raises(ToolExecutionError, match="path escapes"):
        reg.execute("read_text_file", '{"path": "../etc/passwd"}', _ctx(tmp_path))


def test_read_text_file_rejects_binary(tmp_path):
    (tmp_path / "bin.dat").write_bytes(b"\x00\x01\x02")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("read_text_file", '{"path": "bin.dat"}', _ctx(tmp_path))
    assert "binary" in out


def test_write_workspace_text_file(tmp_path):
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute(
        "write_workspace_text_file",
        '{"path": "nested/out.txt", "content": "data"}',
        _ctx(tmp_path),
    )
    assert "wrote:" in out
    assert (tmp_path / "nested" / "out.txt").read_text(encoding="utf-8") == "data"


def test_stat_workspace_path(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("stat_workspace_path", '{"path": "a.txt"}', _ctx(tmp_path))
    payload = json.loads(out)
    assert payload["exists"] is True
    assert payload["is_file"] is True


def test_list_workspace_entries_flat(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("list_workspace_entries", '{"path": "."}', _ctx(tmp_path))
    assert "a.txt" in out and "b.txt" in out


def test_list_workspace_entries_recursive(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "inner.txt").write_text("i", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute(
        "list_workspace_entries",
        '{"path": ".", "recursive": true}',
        _ctx(tmp_path),
    )
    assert "inner.txt" in out


def test_glob_workspace_files(tmp_path):
    (tmp_path / "one.csv").write_text("a", encoding="utf-8")
    (tmp_path / "two.csv").write_text("b", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("glob_workspace_files", '{"pattern": "*.csv"}', _ctx(tmp_path))
    assert "one.csv" in out and "two.csv" in out

