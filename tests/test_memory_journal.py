from multi_agent.memory_journal import MemoryJournal


def test_memory_journal_record_stores_kind_and_key():
    journal = MemoryJournal()
    journal.record("memory_set", key="alpha")
    events = journal.tail()
    assert len(events) == 1
    assert events[0].kind == "memory_set"
    assert events[0].key == "alpha"
    assert "ts" in events[0].payload

