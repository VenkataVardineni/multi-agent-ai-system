"""Save and reload shared memory from a JSON snapshot."""

from multi_agent import SharedMemory


def main() -> None:
    mem = SharedMemory()
    mem.set("plan", "step one")
    mem.save_snapshot("memory_snapshot.json")
    restored = SharedMemory()
    restored.load_snapshot("memory_snapshot.json")
    print(restored.snapshot())


if __name__ == "__main__":
    main()
