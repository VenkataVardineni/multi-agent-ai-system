from multi_agent.memory import SharedMemory


def test_shared_memory_isolation_and_snapshot():
    mem = SharedMemory()
    mem.set("k", {"nested": [1, 2]})
    snap = mem.snapshot()
    mem.set("k", "changed")
    assert snap["k"] == {"nested": [1, 2]}
    assert mem.get("k") == "changed"


def test_shared_memory_thread_safety_basic():
    mem = SharedMemory()
    mem.set("x", 1)
    assert mem.get("x") == 1
