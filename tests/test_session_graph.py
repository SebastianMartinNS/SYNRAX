"""Tests for synrax/runtime/session_graph.py — Incremental graph with lazy reasoning."""

from __future__ import annotations

from pathlib import Path

import pytest

from synrax.namespaces import ARCH
from synrax.runtime.session_graph import SessionGraph


@pytest.fixture()
def project_tree(tmp_path: Path) -> Path:
    """Create a project tree with CodeDNA annotations and real imports."""
    enc = {"encoding": "utf-8"}

    # db/connection.py — leaf module
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

    # models/order.py — imports db.connection
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

    # forms/order_form.py — imports models.order
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

    return tmp_path


class TestSessionGraphBasics:
    def test_init_empty(self, tmp_path: Path):
        sg = SessionGraph(tmp_path)
        assert sg.file_count == 0
        assert sg.raw_triple_count == 0

    def test_ingest_single_file(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        added = sg.ingest_file("db/connection.py")
        assert added > 0
        assert sg.file_count == 1

    def test_ingest_duplicate_returns_zero(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        added = sg.ingest_file("db/connection.py")
        assert added == 0
        assert sg.file_count == 1

    def test_ingest_nonexistent_returns_zero(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        assert sg.ingest_file("nonexistent.py") == 0
        assert sg.file_count == 0

    def test_ingest_non_python_returns_zero(self, project_tree: Path):
        (project_tree / "readme.md").write_text("# Hello", encoding="utf-8")
        sg = SessionGraph(project_tree)
        assert sg.ingest_file("readme.md") == 0


class TestIncrementalIngestion:
    def test_graph_grows_with_each_file(self, project_tree: Path):
        sg = SessionGraph(project_tree)

        sg.ingest_file("db/connection.py")
        count_after_1 = sg.raw_triple_count

        sg.ingest_file("models/order.py")
        count_after_2 = sg.raw_triple_count

        sg.ingest_file("forms/order_form.py")
        count_after_3 = sg.raw_triple_count

        assert count_after_1 > 0
        assert count_after_2 > count_after_1
        assert count_after_3 > count_after_2

    def test_query_results_grow_with_ingestion(self, project_tree: Path):
        sg = SessionGraph(project_tree)

        # Ingest connection only — limited visibility
        sg.ingest_file("db/connection.py")
        results_1 = sg.query_template("impact_analysis", module="db_connection")

        # Ingest order — now order depends on connection
        sg.ingest_file("models/order.py")
        results_2 = sg.query_template("impact_analysis", module="db_connection")

        # More ingested files = potentially more impact results
        assert len(results_2) >= len(results_1)


class TestLazyReasoning:
    def test_dirty_flag_after_ingest(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        assert sg._dirty is True

    def test_reasoning_clears_dirty_flag(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ensure_reasoned()
        assert sg._dirty is False

    def test_re_ingest_sets_dirty_again(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ensure_reasoned()
        assert sg._dirty is False

        sg.ingest_file("models/order.py")
        assert sg._dirty is True

    def test_reasoning_amplifies_triples(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        sg.ingest_file("forms/order_form.py")

        raw = sg.raw_triple_count
        sg.ensure_reasoned()
        reasoned = sg.reasoned_triple_count

        # OWL-RL should infer additional triples (transitive, inverse, etc.)
        assert reasoned >= raw


class TestQueryIntegration:
    def test_impact_analysis_query(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")

        results = sg.query_template("impact_analysis", module="db_connection")
        # models/order.py depends on db/connection.py (via import)
        affected_names = {r.get("name", "") for r in results}
        assert any("models/order" in n for n in affected_names)

    def test_custom_sparql(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")

        results = sg.query(
            "PREFIX arch: <http://archgraph.example.org/> "
            "SELECT ?name WHERE { ?m a arch:Module ; arch:moduleName ?name . }"
        )
        names = {r.get("name", "") for r in results}
        assert "db/connection.py" in names

    def test_ingest_all(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        total = sg.ingest_all()
        assert total > 0
        assert sg.file_count >= 3  # connection, order, order_form
