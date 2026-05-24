# Changelog

## 0.3.1

- `memory_delete` tool and `SharedMemory.delete` remove session keys.
- CLI `workflow --output` writes JSON results to a file.
- `MULTI_AGENT_MOCK_LLM` env enables offline CLI runs without flags.
- `MemoryJournal` supports `len()` for buffered event counts.
- Package exports `WorkflowError`, `ToolExecutionError`, and `MultiAgentError`.
- Docs: security guide, CLI reference, custom tools guide.
- CI and `scripts/coverage.sh` report pytest coverage.
- Examples: memory snapshot demo and coding workflow JSON.
- Tests cover validate CLI, snapshots, prompts, session, and edge tool paths.

## 0.3.0

- Expanded pytest coverage across memory, journal, tools, LLM clients, CLI, and integration paths.
- New `memory_list` tool lists shared session memory keys.
- `SharedMemory.save_snapshot` / `load_snapshot` persist memory to JSON files.
- `ToolRegistry.unregister` removes tools from dynamic registries.
- `DelegationRouter.from_mapping` builds routers from plain dicts.
- CLI adds `validate` subcommand for workflow JSON checks.
- Documentation set: architecture, workflow format, tools, environment, contributing.
- New examples: data profile workflow, custom tool demo, delegation matrix, hooks demo.
- Package exports `Message` type for downstream integrations.

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
- Local verify.sh optionally runs Ruff when installed.
- tiny.csv example aids Data agent demonstrations.
- Pytest coverage expands across loader, retries, hooks, registry helpers, and CLI dry-run.
- Continuous Integration exercises pytest and Ruff on Python 3.10 through 3.12.
- WorkflowStep exposes resolved_write_key() for deterministic orchestration outputs.
- ParsedWorkflow bundles normalized steps plus loader warnings.
- SharedMemory optionally connects to MemoryJournal without breaking callers.
- Tool registry introspection lists deterministic tool_names().
- Agent sessions track loose metadata for downstream integrations.
- Constants module documents MULTI_AGENT_MAX_TOOL_LOOPS and workspace env vars.
