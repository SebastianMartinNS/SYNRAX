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


# ── EXP-5: Edge source tracking ───────────────────────────────────────

class TestEdgeSources:
    """EXP-5: Verify that ingest_file tracks whether edges are structural or annotated."""

    def test_edge_sources_populated(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        # models/order.py imports db.connection → structural edge
        # db/connection.py has used_by: models/order.py → annotated edge
        assert len(sg._edge_sources) > 0

    def test_structural_edge_from_import(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("models/order.py")
        # models/order.py has "from db.connection import get_connection"
        # This creates a structural forward edge
        structural = {k: v for k, v in sg._edge_sources.items() if v == "structural"}
        assert len(structural) > 0

    def test_annotated_edge_from_used_by(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        # db/connection.py has "used_by: models/order.py -> create_order"
        # This creates an annotated reverse edge (models/order dependsOn db/connection)
        annotated = {k: v for k, v in sg._edge_sources.items() if v == "annotated"}
        assert len(annotated) > 0


# ── EXP-2: Visited file tracking ──────────────────────────────────────

class TestVisitedTracking:
    """EXP-2: Verify mark_visited and get_boundary_status."""

    def test_mark_visited_tracks_files(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.mark_visited("db/connection.py")
        assert "db/connection.py" in sg._visited_files

    def test_visited_starts_empty(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        assert len(sg._visited_files) == 0

    def test_boundary_status_empty_when_no_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        status = sg.get_boundary_status()
        assert status == {}

    def test_boundary_status_after_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        sg.mark_visited("db/connection.py")
        sg.mark_visited("models/order.py")
        status = sg.get_boundary_status()
        assert "explored_pct" in status
        assert isinstance(status["explored_pct"], int)
        assert 0 <= status["explored_pct"] <= 100
        assert "remaining_in_scope" in status
        assert "out_of_scope_sample" in status


# ── EXP-3: Node role classification ───────────────────────────────────

class TestNodeRoleClassification:
    """EXP-3: Verify classify_node_roles hub/leaf/connector classification."""

    def test_init_py_is_hub(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        roles = sg.classify_node_roles()
        init_files = [f for f in roles if f.endswith("__init__.py")]
        for f in init_files:
            assert roles[f] == "hub", f"{f} should be classified as hub"

    def test_leaf_modules_classified(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        roles = sg.classify_node_roles()
        # There should be at least one non-hub role
        non_hub = {f: r for f, r in roles.items() if r != "hub"}
        assert len(non_hub) > 0

    def test_all_ingested_files_have_roles(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        roles = sg.classify_node_roles()
        # Every ingested file should have a role
        for f in sg._ingested_files:
            assert f in roles, f"Missing role for {f}"


# ── EXP-5: Architectural level inference ──────────────────────────────

class TestArchitecturalLevel:
    """EXP-5: Verify infer_architectural_level heuristic."""

    def test_init_py_is_routing(self):
        assert SessionGraph.infer_architectural_level("db/__init__.py") == "routing"

    def test_base_dir_is_base_layer(self):
        assert SessionGraph.infer_architectural_level("backends/base/client.py") == "base-layer"

    def test_mysql_is_backend_impl(self):
        assert SessionGraph.infer_architectural_level("backends/mysql/client.py") == "backend-impl"

    def test_postgresql_is_backend_impl(self):
        assert SessionGraph.infer_architectural_level("backends/postgresql/operations.py") == "backend-impl"

    def test_test_file_is_test(self):
        assert SessionGraph.infer_architectural_level("tests/test_client.py") == "test"

    def test_regular_file_is_feature(self):
        assert SessionGraph.infer_architectural_level("models/order.py") == "feature"
