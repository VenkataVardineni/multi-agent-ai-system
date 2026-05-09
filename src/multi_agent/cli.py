from __future__ import annotations

import argparse
import json
import os
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from multi_agent.agents import (
    build_coding_agent,
    build_data_agent,
    build_planner,
    build_research_agent,
    build_reviewer_agent,
    build_writer_agent,
)
from multi_agent.constants import ENV_WORKSPACE
from multi_agent.delegation import DelegationRouter
from multi_agent.llm.mock import MockLLM
from multi_agent.llm.openai_client import OpenAICompatClient
from multi_agent.llm.protocol import ChatClient, ChatResult, ToolCallSpec
from multi_agent.logging_config import configure_logging
from multi_agent.memory import SharedMemory
from multi_agent.orchestrator import Orchestrator
from multi_agent.session import AgentSession
from multi_agent.tools import build_default_registry
from multi_agent.tools.registry import ToolContext, ToolRegistry
from multi_agent.types import AgentRole, Task
from multi_agent.workflow_loader import load_workflow_file


def _package_version() -> str:
    try:
        return version("multi-agent")
    except PackageNotFoundError:
        return "0.0.0"


def _resolve_workspace(cli_value: str | None) -> str:
    if cli_value:
        return cli_value
    return os.environ.get(ENV_WORKSPACE, ".")


def _build_llm(use_mock: bool) -> ChatClient:
    if use_mock:
        return MockLLM(
            responses=[
                ChatResult(
                    content=None,
                    tool_calls=(
                        ToolCallSpec(
                            id="call_1",
                            name="memory_set",
                            arguments=json.dumps({"key": "note", "value": "demo"}),
                        ),
                    ),
                ),
                ChatResult(content="completed-with-tools", tool_calls=()),
            ]
        )
    return OpenAICompatClient()


def _builders_for(registry: ToolRegistry, llm: ChatClient) -> dict[AgentRole, Any]:
    return {
        AgentRole.PLANNER: lambda: build_planner(registry, llm),
        AgentRole.RESEARCH: lambda: build_research_agent(registry, llm),
        AgentRole.CODING: lambda: build_coding_agent(registry, llm),
        AgentRole.DATA: lambda: build_data_agent(registry, llm),
        AgentRole.WRITER: lambda: build_writer_agent(registry, llm),
        AgentRole.REVIEWER: lambda: build_reviewer_agent(registry, llm),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Multi-agent orchestration CLI",
        prog="multi-agent",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {_package_version()}",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--json-out",
        action="store_true",
        help="Emit logs as JSON lines on stderr",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    delegate = sub.add_parser("delegate", help="Route a message to an agent")
    delegate.add_argument("message")
    delegate.add_argument(
        "--role",
        choices=[r.value for r in AgentRole],
        default=None,
        help="Force a specific agent role instead of automatic routing",
    )
    delegate.add_argument("--mock-llm", action="store_true")
    delegate.add_argument("--workspace", default=None)

    agent_cmd = sub.add_parser("agent", help="Run a single agent role")
    agent_cmd.add_argument("--role", required=True, choices=[r.value for r in AgentRole])
    agent_cmd.add_argument("--task", required=True)
    agent_cmd.add_argument("--mock-llm", action="store_true")
    agent_cmd.add_argument("--workspace", default=None)

    workflow = sub.add_parser("workflow", help="Run an orchestrated workflow JSON file")
    workflow.add_argument("--file", required=True)
    workflow.add_argument("--mock-llm", action="store_true")
    workflow.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate workflow JSON and print planned steps without executing agents",
    )

    args = parser.parse_args(argv)

    configure_logging(verbose=args.verbose, json_mode=args.json_out)

    registry = build_default_registry()

    if args.command == "delegate":
        llm = _build_llm(args.mock_llm)
        router = DelegationRouter()
        role = AgentRole(args.role) if args.role else router.route(args.message)
        builders_plain = _builders_for(registry, llm)
        agent = builders_plain[role]()
        workspace = _resolve_workspace(args.workspace)
        session_mem = SharedMemory()
        ctx = ToolContext(memory=session_mem, workspace_dir=workspace)
        task = Task(id="delegated-1", description=args.message, role=role)
        result = agent.run(task, ctx)
        payload = {"role": role.value, "output": result}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "agent":
        llm = _build_llm(args.mock_llm)
        role = AgentRole(args.role)
        builders_plain = _builders_for(registry, llm)
        agent = builders_plain[role]()
        workspace = _resolve_workspace(args.workspace)
        session_mem = SharedMemory()
        ctx = ToolContext(memory=session_mem, workspace_dir=workspace)
        task = Task(id="single-1", description=args.task, role=role)
        result = agent.run(task, ctx)
        print(result)
        return 0

    if args.command == "workflow":
        llm = _build_llm(args.mock_llm)
        path = Path(args.file)
        parsed = load_workflow_file(path)

        if parsed.warnings:
            for warning in parsed.warnings:
                print(f"warning:{warning}", file=sys.stderr)

        if args.dry_run:
            summary = {
                "workspace": parsed.workspace,
                "warnings": list(parsed.warnings),
                "steps": [step.to_wire_dict() for step in parsed.steps],
            }
            print(json.dumps(summary, indent=2))
            return 0

        workspace = str(parsed.workspace or ".")
        memory = SharedMemory()
        session = AgentSession(memory=memory, registry=registry, workspace_dir=workspace)

        orchestrator = Orchestrator(_builders_for(registry, llm))

        outputs = orchestrator.run_workflow(
            steps=parsed.steps,
            memory=session.memory,
            workspace_dir=session.workspace_dir,
        )
        print(json.dumps({"outputs": outputs, "memory": memory.snapshot()}, indent=2))
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
