import pytest

from multi_agent.llm.openai_client import OpenAICompatClient


def test_openai_client_missing_key():
    client = OpenAICompatClient(api_key="")
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        client.chat([{"role": "user", "content": "hi"}], None)

import json

import httpx


def test_openai_client_parses_tool_calls(monkeypatch):
    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        def post(self, url, headers=None, content=None):
            payload = {
                "choices": [
                    {
                        "message": {
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": "c1",
                                    "function": {"name": "memory_set", "arguments": "{}"},
                                }
                            ],
                        }
                    }
                ]
            }
            req = httpx.Request("POST", url)
            return httpx.Response(200, content=json.dumps(payload).encode(), request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    client = OpenAICompatClient(api_key="test-key")
    result = client.chat([{"role": "user", "content": "go"}], [])
    assert result.tool_calls[0].name == "memory_set"


def test_openai_client_http_status_error(monkeypatch):
    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        def post(self, url, headers=None, content=None):
            req = httpx.Request("POST", url)
            return httpx.Response(401, text="unauthorized", request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    client = OpenAICompatClient(api_key="bad")
    with pytest.raises(RuntimeError, match="HTTP 401"):
        client.chat([{"role": "user", "content": "hi"}], None)

