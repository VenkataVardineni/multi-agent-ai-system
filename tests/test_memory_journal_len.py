"""Tests for MemoryJournal helpers."""

from multi_agent.memory_journal import MemoryJournal


def test_memory_journal_len():
    journal = MemoryJournal()
    assert len(journal) == 0
    journal.record("tick")
    journal.record("tick")
    assert len(journal) == 2
