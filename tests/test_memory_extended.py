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


def test_shared_memory_namespace():
    mem = SharedMemory(namespace="session-1")
    assert mem.namespace == "session-1"

import threading


def test_shared_memory_concurrent_writes():
    mem = SharedMemory()
    def writer(start: int):
        for i in range(50):
            mem.set(f"k{start + i}", start + i)

    threads = [threading.Thread(target=writer, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(mem.keys()) == 200

