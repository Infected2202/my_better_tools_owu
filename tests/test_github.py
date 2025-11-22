import asyncio
import os
import sys
from pydantic import Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.github import Tools


def test_list_repository_files_normalizes_non_string_path(monkeypatch):
    tool = Tools()
    monkeypatch.setattr(tool, "_split_repo", lambda repo: ("owner", "repo"))

    calls = {}

    def fake_make_request(endpoint, params):
        calls["endpoint"] = endpoint
        calls["params"] = params
        return []

    monkeypatch.setattr(tool, "_make_request", fake_make_request)

    result = asyncio.run(
        tool.list_repository_files(repo="owner/repo", path=Field(default=""))
    )

    assert calls["endpoint"] == "/repos/owner/repo/contents/"
    assert calls["params"] == {}
    assert "*Empty directory*" in result


def test_list_repository_files_quotes_path(monkeypatch):
    tool = Tools()
    monkeypatch.setattr(tool, "_split_repo", lambda repo: ("owner", "repo"))

    calls = {}

    def fake_make_request(endpoint, params):
        calls["endpoint"] = endpoint
        calls["params"] = params
        return []

    monkeypatch.setattr(tool, "_make_request", fake_make_request)

    result = asyncio.run(tool.list_repository_files(repo="owner/repo", path="dir name"))

    assert calls["endpoint"] == "/repos/owner/repo/contents/dir%20name"
    assert calls["params"] == {}
    assert "# Contents: owner/repo/dir name" in result
