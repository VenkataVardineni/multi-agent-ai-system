"""Restricted Python snippet execution for agent code tasks."""

from __future__ import annotations

import ast
from typing import Any

from multi_agent.tools.registry import ToolContext, ToolDefinition

_SAFE_BUILTINS: dict[str, Any] = {
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}


class _UnsafeAst(Exception):
    pass


def _validate_stmt(node: ast.stmt) -> None:
    allowed = (
        ast.Assign,
        ast.AugAssign,
        ast.Expr,
        ast.If,
        ast.For,
        ast.While,
        ast.Pass,
        ast.Break,
        ast.Continue,
        ast.FunctionDef,
        ast.Return,
    )
    if not isinstance(node, allowed):
        raise _UnsafeAst(f"disallowed statement: {type(node).__name__}")


def _validate_expr(node: ast.expr) -> None:
    banned_calls = {
        "open",
        "compile",
        "exec",
        "eval",
        "__import__",
        "globals",
        "locals",
        "getattr",
        "setattr",
        "delattr",
    }
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name) and child.func.id in banned_calls:
                raise _UnsafeAst(f"banned call: {child.func.id}")


def _safe_exec(code: str, inject: dict[str, Any]) -> Any:
    tree = ast.parse(code, mode="exec")
    for stmt in tree.body:
        _validate_stmt(stmt)
        for sub in ast.walk(stmt):
            if isinstance(sub, ast.expr):
                _validate_expr(sub)

    global_ns: dict[str, Any] = {"__builtins__": _SAFE_BUILTINS}
    local_ns: dict[str, Any] = dict(inject)
    exec(compile(tree, filename="<agent_snippet>", mode="exec"), global_ns, local_ns)
    return local_ns.get("result", None)


def _run_python_snippet(ctx: ToolContext, args: dict[str, Any]) -> str:
    code = str(args["code"])
    memory_keys = args.get("memory_keys") or []
    inject: dict[str, Any] = {}
    if isinstance(memory_keys, list):
        for key in memory_keys:
            inject[str(key)] = ctx.memory.get(str(key))
    try:
        result = _safe_exec(code, inject)
    except _UnsafeAst as exc:
        return f"error:unsafe:{exc}"
    except Exception as exc:  # noqa: BLE001
        return f"error:{exc}"
    return str(result)


def code_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="run_python_snippet",
            description=(
                "Execute a restricted Python snippet with injected memory values. "
                "Set the variable `result` to return a value."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "memory_keys": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["code"],
            },
            handler=_run_python_snippet,
        )
    ]
