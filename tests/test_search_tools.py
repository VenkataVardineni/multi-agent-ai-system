from multi_agent.memory import SharedMemory
from multi_agent.tools.registry import ToolContext, ToolRegistry
from multi_agent.tools.search_tools import search_tool_definitions


def test_web_search_stub(tmp_path):
    reg = ToolRegistry(search_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("web_search_stub", '{"query": "multi agent"}', ctx)
    assert "multi agent" in out

import httpx


def test_fetch_url_text_success(tmp_path, monkeypatch):
    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        def get(self, url, headers=None):
            req = httpx.Request("GET", url)
            return httpx.Response(200, text="hello web", request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    reg = ToolRegistry(search_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("fetch_url_text", '{"url": "https://example.com"}', ctx)
    assert out == "hello web"


def test_fetch_url_text_http_error(tmp_path, monkeypatch):
    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        def get(self, url, headers=None):
            req = httpx.Request("GET", url)
            return httpx.Response(404, request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    reg = ToolRegistry(search_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("fetch_url_text", '{"url": "https://example.com/missing"}', ctx)
    assert out.startswith("error:http:")

