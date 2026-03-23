"""Tests for the CLI serve command (stdio JSON-RPC)."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from synrax.cli.main import cli


@pytest.fixture()
def codebase(tmp_path: Path) -> Path:
    """Create a minimal codebase for serve testing."""
    root = tmp_path / "project"
    root.mkdir()
    (root / ".codedna").write_text(
        "project: test\npackages:\n  core/:\n    purpose: core logic\n",
        encoding="utf-8",
    )
    core = root / "core"
    core.mkdir()
    (core / "base.py").write_text(
        '"""core/base.py -- Base utilities.\n\n'
        "exports: setup() -> None\n"
        "used_by: core/app.py -> init\n"
        "rules:   Must init before use.\n"
        '"""\ndef setup(): pass\n',
        encoding="utf-8",
    )
    (core / "app.py").write_text(
        '"""core/app.py -- Application entry.\n\n'
        "exports: init() -> None\n"
        "used_by: none\n"
        "rules:   none\n"
        '"""\nfrom core.base import setup\ndef init(): setup()\n',
        encoding="utf-8",
    )
    return root


def _invoke_serve(codebase: Path, requests: list[dict], pre_ingest: bool = False) -> list[dict]:
    """Invoke serve via CliRunner, return parsed JSON responses from stdout."""
    runner = CliRunner()
    input_text = "\n".join(json.dumps(r) for r in requests) + "\n"

    args = ["serve", str(codebase)]
    if pre_ingest:
        args.append("--pre-ingest")

    result = runner.invoke(cli, args, input=input_text)
    stdout_lines = [l for l in result.output.strip().splitlines() if l.strip()]
    parsed = []
    for line in stdout_lines:
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return parsed


class TestServeIngest:
    def test_ingest_file(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest",
             "params": {"path": "core/base.py"}},
        ])
        assert len(responses) >= 1
        assert responses[0]["id"] == 1
        assert responses[0]["result"]["triples_added"] > 0

    def test_ingest_then_status(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest",
             "params": {"path": "core/base.py"}},
            {"jsonrpc": "2.0", "id": 2, "method": "synrax.status", "params": {}},
        ])
        assert len(responses) >= 2
        assert "1 files ingested" in responses[1]["result"]["text"]


class TestServeQuery:
    def test_query_impact(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest",
             "params": {"path": "core/base.py"}},
            {"jsonrpc": "2.0", "id": 2, "method": "synrax.ingest",
             "params": {"path": "core/app.py"}},
            {"jsonrpc": "2.0", "id": 3, "method": "synrax.query_impact",
             "params": {"module": "core/base.py"}},
        ])
        assert len(responses) >= 3
        assert "result" in responses[2]

    def test_query_deps(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest",
             "params": {"path": "core/app.py"}},
            {"jsonrpc": "2.0", "id": 2, "method": "synrax.query_deps",
             "params": {"module": "core/app.py"}},
        ])
        assert len(responses) >= 2
        assert "result" in responses[1]

    def test_query_rules(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest",
             "params": {"path": "core/base.py"}},
            {"jsonrpc": "2.0", "id": 2, "method": "synrax.query_rules",
             "params": {"module": "core/base.py"}},
        ])
        assert len(responses) >= 2
        assert "result" in responses[1]
        assert "Must init" in responses[1]["result"]["text"]


class TestServeErrors:
    def test_method_not_found(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "bogus.method", "params": {}},
        ])
        assert len(responses) >= 1
        assert "error" in responses[0]
        assert responses[0]["error"]["code"] == -32601

    def test_missing_param(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.ingest", "params": {}},
        ])
        assert len(responses) >= 1
        assert "error" in responses[0]
        assert responses[0]["error"]["code"] == -32602


class TestServePreIngest:
    def test_pre_ingest_flag(self, codebase: Path) -> None:
        responses = _invoke_serve(codebase, [
            {"jsonrpc": "2.0", "id": 1, "method": "synrax.status", "params": {}},
        ], pre_ingest=True)
        assert len(responses) >= 1
        assert "2 files ingested" in responses[0]["result"]["text"]
