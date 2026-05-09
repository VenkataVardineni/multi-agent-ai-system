# Changelog

## 0.2.0

- Weighted delegation scoring with reviewer-aware tie breaking.
- Structured workflow loader surfaces duplicate write_key warnings.
- Optional MemoryJournal records SharedMemory writes for tracing.
- Orchestrator accepts OrchestrationHooks for step lifecycle telemetry.
- Filesystem tools now cover stat, recursive listing, globs, and atomic writes.
- Research tooling adds fetch_url_text with byte caps and UTF-8 decoding guards.
- RetryingChatClient wraps ChatClient calls with exponential backoff.
