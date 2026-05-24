from multi_agent.memory_journal import MemoryJournal


def test_memory_journal_record_stores_kind_and_key():
    journal = MemoryJournal()
    journal.record("memory_set", key="alpha")
    events = journal.tail()
    assert len(events) == 1
    assert events[0].kind == "memory_set"
    assert events[0].key == "alpha"
    assert "ts" in events[0].payload


def test_memory_journal_tail_limit_and_ring_buffer():
    journal = MemoryJournal(max_events=20)
    for i in range(30):
        journal.record("tick", key=str(i))
    tail = journal.tail(limit=5)
    assert len(tail) == 5
    assert tail[-1].key == "29"
    assert len(journal.tail(limit=100)) == 20

