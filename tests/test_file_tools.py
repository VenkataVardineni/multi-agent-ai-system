
def test_list_entries_not_directory(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("x", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("list_workspace_entries", '{"path": "file.txt"}', _ctx(tmp_path))
    assert "not a directory" in out


def test_glob_respects_limit(tmp_path):
    for i in range(5):
        (tmp_path / f"f{i}.txt").write_text("x", encoding="utf-8")
    reg = ToolRegistry(file_tool_definitions())
    out = reg.execute("glob_workspace_files", '{"pattern": "*.txt", "limit": 2}', _ctx(tmp_path))
    import json
    matches = json.loads(out)["matches"]
    assert len(matches) == 2

