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

