# CLI reference

```bash
multi-agent --version
multi-agent delegate "<message>" [--role ROLE] [--mock-llm] [--workspace PATH]
multi-agent agent --role ROLE --task "<text>" [--mock-llm] [--workspace PATH]
multi-agent validate --file workflow.json
multi-agent workflow --file workflow.json [--mock-llm] [--dry-run] [--output PATH]
```

Global flags: `--verbose`, `--json-out`.

Environment: see [environment.md](environment.md). Offline shortcut: `MULTI_AGENT_MOCK_LLM=1`.
