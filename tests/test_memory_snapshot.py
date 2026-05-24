import json

from multi_agent.memory import SharedMemory


def test_save_and_load_snapshot_roundtrip(tmp_path):
    mem = SharedMemory()
    mem.set("note", {"x": 1})
    path = tmp_path / "snap.json"
    mem.save_snapshot(path)
    other = SharedMemory()
    other.load_snapshot(path)
    assert other.get("note") == {"x": 1}


def test_load_snapshot_rejects_non_object(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps([1, 2]), encoding="utf-8")
    mem = SharedMemory()
    try:
        mem.load_snapshot(path)
    except ValueError as exc:
        assert "JSON object" in str(exc)
    else:
        raise AssertionError("expected ValueError")

