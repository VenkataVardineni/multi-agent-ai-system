# Security boundaries

## Workspace sandbox

File tools resolve paths under the configured workspace. Paths containing `..` that escape the workspace raise an error.

## Restricted Python

`run_python_snippet` validates AST nodes and blocks dangerous builtins (`open`, `eval`, `__import__`, etc.).

## HTTP fetches

`fetch_url_text` truncates responses and rejects binary payloads. Use timeouts and treat remote content as untrusted input.

## Live LLM calls

Set `OPENAI_API_KEY` only in trusted environments. Prefer `--mock-llm` or `MULTI_AGENT_MOCK_LLM=1` for offline runs.
