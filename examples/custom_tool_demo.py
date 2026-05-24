"""Register a custom tool alongside the default bundle."""

from multi_agent.memory import SharedMemory
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext, ToolDefinition


def _echo(ctx: ToolContext, args: dict) -> str:
    return str(args.get("text", ""))


def main() -> None:
    registry = build_default_registry()
    registry.register(
        ToolDefinition(
            name="echo",
            description="Echo text for demos",
            parameters={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
            handler=_echo,
        )
    )
    ctx = ToolContext(memory=SharedMemory())
    print(registry.execute("echo", '{"text": "hello"}', ctx))


if __name__ == "__main__":
    main()
