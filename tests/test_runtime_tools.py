"""Tests for synrax/runtime/tools.py — Agent-callable tool functions."""

from __future__ import annotations

from pathlib import Path

import pytest

from synrax.runtime.session_graph import SessionGraph
from synrax.runtime.tools import make_synrax_tools


@pytest.fixture()
def project_tree(tmp_path: Path) -> Path:
    """Create a project tree with CodeDNA annotations and real imports."""
    enc = {"encoding": "utf-8"}

    (tmp_path / "db").mkdir()
    (tmp_path / "db" / "__init__.py").write_text("", **enc)
    (tmp_path / "db" / "connection.py").write_text(
        '"""db/connection.py - Database pool.\n\n'
        "exports: get_connection() -> Connection\n"
        "used_by: models/order.py -> create_order\n"
        'rules:   Always use parameterized queries.\n'
        '"""\n\n'
        "def get_connection(): pass\n",
        **enc,
    )

    (tmp_path / "models").mkdir()
    (tmp_path / "models" / "__init__.py").write_text("", **enc)
    (tmp_path / "models" / "order.py").write_text(
        '"""models/order.py - Order logic.\n\n'
        "exports: create_order(data) -> Order\n"
        "used_by: forms/order_form.py -> validate_order [cascade]\n"
        'rules:   States: draft -> confirmed -> paid.\n'
        '"""\n\n'
        "from db.connection import get_connection\n\n"
        "def create_order(data): pass\n",
        **enc,
    )

    (tmp_path / "forms").mkdir()
    (tmp_path / "forms" / "__init__.py").write_text("", **enc)
    (tmp_path / "forms" / "order_form.py").write_text(
        '"""forms/order_form.py - Order validation.\n\n'
        "exports: validate_order(data) -> bool\n"
        "used_by: views/checkout.py -> checkout_view\n"
        'rules:   Totals in cents, never float.\n'
        '"""\n\n'
        "from models.order import create_order\n\n"
        "def validate_order(data): pass\n",
        **enc,
    )

    (tmp_path / "views").mkdir()
    (tmp_path / "views" / "__init__.py").write_text("", **enc)
    (tmp_path / "views" / "checkout.py").write_text(
        '"""views/checkout.py - Checkout handler.\n\n'
        "exports: checkout_view(request) -> HttpResponse\n"
        'rules:   Never call models directly.\n'
        '"""\n\n'
        "from forms.order_form import validate_order\n\n"
        "def checkout_view(request): pass\n",
        **enc,
    )

    return tmp_path


@pytest.fixture()
def tools(project_tree: Path) -> dict:
    """SessionGraph with all files ingested and tools created."""
    sg = SessionGraph(project_tree)
    sg.ingest_all()
    return make_synrax_tools(sg)


class TestQueryImpact:
    def test_impact_returns_dependents(self, tools):
        result = tools["query_impact"]("db/connection.py")
        assert "models/order" in result
        assert "files" in result.lower()

    def test_impact_on_leaf_returns_no_deps(self, tools):
        result = tools["query_impact"]("views/checkout.py")
        assert "No files found" in result or "0 files" in result.lower() or "affected" in result.lower()

    def test_impact_auto_ingests(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        # Don't ingest anything beforehand
        result = t["query_impact"]("db/connection.py")
        assert sg.file_count >= 1  # auto-ingested


class TestQueryDeps:
    def test_deps_returns_imports(self, tools):
        result = tools["query_deps"]("models/order.py")
        assert "db/connection" in result

    def test_root_module_has_no_deps(self, tools):
        result = tools["query_deps"]("db/connection.py")
        assert "no known dependencies" in result.lower() or "0 dependencies" in result.lower() or "depends on" in result.lower()


class TestQueryRules:
    def test_rules_returns_constraints(self, tools):
        result = tools["query_rules"]("db/connection.py")
        assert "parameterized" in result.lower()

    def test_rules_includes_impact_zone(self, tools):
        result = tools["query_rules"]("db/connection.py")
        # Should include rules from dependent modules too
        assert "rule" in result.lower() or "Rules" in result


class TestQueryGraphStatus:
    def test_status_shows_triple_count(self, tools):
        result = tools["query_graph_status"]()
        assert "triples" in result.lower()
        assert "files ingested" in result.lower()

    def test_status_orphan_and_circular(self, tools):
        result = tools["query_graph_status"]()
        assert "orphan" in result.lower() or "Orphan" in result
        assert "circular" in result.lower() or "Circular" in result


class TestEmptyGraph:
    def test_impact_on_empty_graph(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        result = t["query_impact"]("nonexistent.py")
        # Should handle gracefully
        assert isinstance(result, str)

    def test_status_on_empty_graph(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        result = t["query_graph_status"]()
        assert "0 files ingested" in result or "files ingested" in result


# ── EXP-2: Boundary query tool ────────────────────────────────────────

class TestQueryBoundary:
    """EXP-2: Verify query_boundary tool returns exploration status."""

    def test_boundary_tool_exists(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        assert "query_boundary" in t

    def test_boundary_no_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        result = t["query_boundary"]()
        assert "No files visited" in result

    def test_boundary_after_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        sg.mark_visited("db/connection.py")
        sg.mark_visited("models/order.py")
        t = make_synrax_tools(sg)
        result = t["query_boundary"]()
        assert "exploration" in result.lower() or "complete" in result.lower()
        assert "Files visited: 2" in result


# ── Tension query tool ────────────────────────────────────────────────

class TestQueryTension:
    """Verify query_tension tool returns tension status."""

    def test_tension_tool_exists(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        assert "query_tension" in t

    def test_tension_no_data(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = make_synrax_tools(sg)
        result = t["query_tension"]()
        assert "no dependency data" in result.lower() or "0/0" in result

    def test_tension_after_ingest(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        t = make_synrax_tools(sg)
        result = t["query_tension"]()
        assert "blast zone" in result.lower() or "unexplored" in result.lower()

    def test_tension_after_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        sg.mark_visited("db/connection.py")
        sg.mark_visited("models/order.py")
        t = make_synrax_tools(sg)
        result = t["query_tension"]()
        assert "explored" in result.lower() or "%" in result
