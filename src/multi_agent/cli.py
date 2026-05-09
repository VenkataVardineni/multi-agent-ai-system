from __future__ import annotations

import argparse
import json
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
from multi_agent.types import AgentRole, Task, WorkflowStep


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


def _workflow_steps_from_json(payload: dict[str, Any]) -> list[WorkflowStep]:
    raw_steps = payload.get("steps") or []
    steps: list[WorkflowStep] = []
    for item in raw_steps:
        role = AgentRole(str(item["role"]))
        instruction = str(item["instruction"])
        read_keys = tuple(str(k) for k in item.get("read_keys", []) or [])
        write_key = item.get("write_key")
        steps.append(
            WorkflowStep(
                role=role,
                instruction=instruction,
                read_keys=read_keys,
                write_key=str(write_key) if write_key else None,
            )
        )
    return steps


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
    parser = argparse.ArgumentParser(description="Multi-agent orchestration CLI")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--json-out",
        action="store_true",
        help="Emit logs as JSON lines on stderr",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    delegate = sub.add_parser("delegate", help="Route a message to an agent")
    delegate.add_argument("message")
    delegate.add_argument("--mock-llm", action="store_true")
    delegate.add_argument("--workspace", default=".")

    agent_cmd = sub.add_parser("agent", help="Run a single agent role")
    agent_cmd.add_argument("--role", required=True, choices=[r.value for r in AgentRole])
    agent_cmd.add_argument("--task", required=True)
    agent_cmd.add_argument("--mock-llm", action="store_true")
    agent_cmd.add_argument("--workspace", default=".")

    workflow = sub.add_parser("workflow", help="Run an orchestrated workflow JSON file")
    workflow.add_argument("--file", required=True)
    workflow.add_argument("--mock-llm", action="store_true")

    args = parser.parse_args(argv)

    configure_logging(verbose=args.verbose, json_mode=args.json_out)

    registry = build_default_registry()

    if args.command == "delegate":
        llm = _build_llm(args.mock_llm)
        router = DelegationRouter()
        role = router.route(args.message)
        builders_plain = _builders_for(registry, llm)
        agent = builders_plain[role]()
        session_mem = SharedMemory()
        ctx = ToolContext(memory=session_mem, workspace_dir=args.workspace)
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
        session_mem = SharedMemory()
        ctx = ToolContext(memory=session_mem, workspace_dir=args.workspace)
        task = Task(id="single-1", description=args.task, role=role)
        result = agent.run(task, ctx)
        print(result)
        return 0

    if args.command == "workflow":
        llm = _build_llm(args.mock_llm)
        path = Path(args.file)
        payload = json.loads(path.read_text(encoding="utf-8"))
        steps = _workflow_steps_from_json(payload)
        workspace = str(payload.get("workspace") or ".")

        memory = SharedMemory()
        session = AgentSession(memory=memory, registry=registry, workspace_dir=workspace)

        orchestrator = Orchestrator(_builders_for(registry, llm))

        outputs = orchestrator.run_workflow(
            steps=steps,
            memory=session.memory,
            workspace_dir=session.workspace_dir,
        )
        print(json.dumps({"outputs": outputs, "memory": memory.snapshot()}, indent=2))
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
