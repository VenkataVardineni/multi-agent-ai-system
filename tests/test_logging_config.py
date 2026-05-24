import json
import logging

from multi_agent.logging_config import configure_logging


def test_configure_logging_json(capsys):
    configure_logging(verbose=True, json_mode=True)
    logging.getLogger("test").info("hello-json")
    captured = capsys.readouterr()
    line = captured.err.strip().splitlines()[-1]
    payload = json.loads(line)
    assert payload["message"] == "hello-json"
    assert payload["level"] == "INFO"

