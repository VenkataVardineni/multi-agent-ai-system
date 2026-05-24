
def test_fetch_url_text_binary(tmp_path, monkeypatch):
    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        def get(self, url, headers=None):
            req = httpx.Request("GET", url)
            return httpx.Response(200, content=b"\x00\x01", request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    reg = ToolRegistry(search_tool_definitions())
    ctx = ToolContext(memory=SharedMemory(), workspace_dir=str(tmp_path))
    out = reg.execute("fetch_url_text", '{"url": "https://example.com/bin"}', ctx)
    assert "binary" in out

