# Changelog

## 0.2.0

- Weighted delegation scoring with reviewer-aware tie breaking.
- Structured workflow loader surfaces duplicate write_key warnings.
- Optional MemoryJournal records SharedMemory writes for tracing.
- Orchestrator accepts OrchestrationHooks for step lifecycle telemetry.
- Filesystem tools now cover stat, recursive listing, globs, and atomic writes.
- Research tooling adds fetch_url_text with byte caps and UTF-8 decoding guards.
- RetryingChatClient wraps ChatClient calls with exponential backoff.
- OpenAI-compatible client raises descriptive errors when HTTP responses fail.
- MockLLM.reset rewinds scripted chats for repeatable tests.
- CLI learns workflow --dry-run, delegate --role overrides, and MULTI_AGENT_WORKSPACE defaults.
- Package exports highlight ParsedWorkflow, hooks, and MemoryJournal helpers.
- MIT LICENSE file ships alongside classifier metadata.
- README documents MULTI_AGENT_* environment shortcuts and new CLI switches.
