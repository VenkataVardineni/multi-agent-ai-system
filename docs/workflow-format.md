# Workflow JSON format

```json
{
  "workspace": ".",
  "steps": [
    {
      "role": "planner",
      "instruction": "Outline the task",
      "read_keys": [],
      "write_key": "plan",
      "label": "Planning"
    }
  ]
}
```

## Fields

- `workspace` — optional directory passed to tool handlers.
- `steps` — required list of step objects.
- `role` — one of `planner`, `research`, `coding`, `data`, `writer`, `reviewer`.
- `instruction` — prompt text for the agent.
- `read_keys` — memory keys injected into the instruction.
- `write_key` — optional memory key for the step output (defaults to `{role}_step_{index}`).
- `label` — optional human-readable label for logging.
