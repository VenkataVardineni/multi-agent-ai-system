from multi_agent.memory import SharedMemory


def test_shared_memory_keys_contains_and_default():
    mem = SharedMemory()
    mem.set("a", 1)
    assert "a" in mem
    assert "b" not in mem
    assert mem.get("missing", "fallback") == "fallback"
    assert sorted(mem.keys()) == ["a"]


def test_shared_memory_merge_snapshot():
    mem = SharedMemory()
    mem.merge_snapshot({"x": 1, "y": 2})
    assert mem.get("x") == 1
    mem.merge_snapshot({"y": 99})
    assert mem.get("y") == 99

