# Adding custom tools

```python
from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext, ToolDefinition

def echo_handler(ctx: ToolContext, args: dict) -> str:
    return str(args.get("text", ""))

registry = build_default_registry()
registry.register(
    ToolDefinition(
        name="echo",
        description="Echo input text",
        parameters={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        handler=echo_handler,
    )
)
```

See `examples/custom_tool_demo.py` for a runnable script.
