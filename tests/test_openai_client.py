import httpx
import pytest

from multi_agent.llm.openai_client import OpenAICompatClient


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

