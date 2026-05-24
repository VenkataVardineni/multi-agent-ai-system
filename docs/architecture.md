# Architecture

The multi-agent runtime coordinates specialized agents through a shared tool registry,
session memory, and optional workflow orchestration.

## Layers

1. **CLI** — `delegate`, `agent`, `workflow`, and `validate` commands.
2. **Orchestrator** — runs ordered `WorkflowStep` lists with memory injection.
3. **Agents** — `BaseAgent` tool-calling loop backed by a `ChatClient`.
4. **Tools** — sandboxed filesystem, memory, CSV, code, and search helpers.
5. **LLM** — OpenAI-compatible client, retry wrapper, and offline `MockLLM`.

See the README mermaid diagram for a quick visual overview.
