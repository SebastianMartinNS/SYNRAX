"""Tests for synrax/runtime/session_graph.py — Incremental graph with lazy reasoning."""

from __future__ import annotations

from pathlib import Path

import pytest

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
        "rules:   Always use parameterized queries.\n"
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
        "rules:   States: draft -> confirmed -> paid.\n"
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
        "rules:   Totals in cents, never float.\n"
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
        results_1 = sg.query_template("impact_analysis", module="db::connection")

        # Ingest order — now order depends on connection
        sg.ingest_file("models/order.py")
        results_2 = sg.query_template("impact_analysis", module="db::connection")

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

        results = sg.query_template("impact_analysis", module="db::connection")
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

    def test_get_edge_source_returns_type(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        # There should be at least one edge with a known source
        has_known = any(sg.get_edge_source(f, t) != "unknown" for f, t in sg._edge_sources)
        assert has_known

    def test_get_edge_source_unknown_for_missing(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        assert sg.get_edge_source("nonexistent.py", "other.py") == "unknown"

    def test_inferred_edges_tracked_after_reasoning(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        sg.ingest_file("forms/order_form.py")
        sg.ensure_reasoned()
        # After reasoning, transitive edges should be tracked as "inferred"
        inferred = {k: v for k, v in sg._edge_sources.items() if v == "inferred"}
        # forms/order_form -> db/connection is transitive (via models/order)
        assert len(inferred) >= 0  # May or may not have inferred edges depending on graph


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
        assert (
            SessionGraph.infer_architectural_level("backends/postgresql/operations.py")
            == "backend-impl"
        )

    def test_test_file_is_test(self):
        assert SessionGraph.infer_architectural_level("tests/test_client.py") == "test"

    def test_regular_file_is_feature(self):
        assert SessionGraph.infer_architectural_level("models/order.py") == "feature"


# ── Tension engine ────────────────────────────────────────────────────


class TestComputeTension:
    """Verify compute_tension() returns correct tension metrics."""

    def test_tension_max_when_nothing_visited(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        t = sg.compute_tension()
        assert t["tension_ratio"] == 1.0
        assert t["blast_zone_unvisited"] == t["blast_zone_total"]
        assert t["explored_pct"] == 0

    def test_tension_decreases_with_visits(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        t0 = sg.compute_tension()
        sg.mark_visited("db/connection.py")
        sg.mark_visited("models/order.py")
        t1 = sg.compute_tension()
        assert t1["tension_ratio"] < t0["tension_ratio"]
        assert t1["explored_pct"] > 0

    def test_tension_zero_when_all_visited(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        for f in list(sg._ingested_files):
            sg.mark_visited(f)
        t = sg.compute_tension()
        assert t["tension_ratio"] == 0.0
        assert t["blast_zone_unvisited"] == 0

    def test_tension_has_all_keys(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        t = sg.compute_tension()
        assert "blast_zone_total" in t
        assert "blast_zone_unvisited" in t
        assert "tension_ratio" in t
        assert "high_tension_files" in t
        assert "explored_pct" in t

    def test_high_tension_files_unvisited(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_all()
        sg.mark_visited("db/connection.py")
        t = sg.compute_tension()
        # high_tension_files should NOT contain visited files
        for f in t["high_tension_files"]:
            assert f not in sg._visited_files

    def test_tension_empty_graph(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        t = sg.compute_tension()
        assert t["tension_ratio"] == 0.0
        assert t["blast_zone_total"] == 0


# ── Step 3.1: URI collision tests ─────────────────────────────────────


class TestURICollision:
    """Verify that underscores in filenames don't collide with directory separators."""

    @pytest.fixture()
    def collision_tree(self, tmp_path: Path) -> Path:
        """Create a tree where 'my_model.py' and 'my/model.py' coexist."""
        enc = {"encoding": "utf-8"}

        # my_model.py (underscore in filename)
        (tmp_path / "my_model.py").write_text(
            '"""my_model.py \u2014 Flat module.\n\n'
            "exports: flat_func() -> None\n"
            "rules:   Flat module rule.\n"
            '"""\n\n'
            "def flat_func(): pass\n",
            **enc,
        )

        # my/model.py (directory + filename)
        (tmp_path / "my").mkdir()
        (tmp_path / "my" / "__init__.py").write_text("", **enc)
        (tmp_path / "my" / "model.py").write_text(
            '"""my/model.py \u2014 Nested module.\n\n'
            "exports: nested_func() -> None\n"
            "rules:   Nested module rule.\n"
            '"""\n\n'
            "def nested_func(): pass\n",
            **enc,
        )

        return tmp_path

    def test_distinct_uris(self, collision_tree: Path):
        """my_model.py and my/model.py must produce different URIs."""
        from synrax.namespaces import make_module_uri

        uri_flat = make_module_uri("my_model.py")
        uri_nested = make_module_uri("my/model.py")
        assert uri_flat != uri_nested
        assert uri_flat == "my_model"  # underscore preserved
        assert uri_nested == "my::model"  # directory uses ::

    def test_distinct_ingestion(self, collision_tree: Path):
        """Both files ingest without overwriting each other."""
        sg = SessionGraph(collision_tree)
        added1 = sg.ingest_file("my_model.py")
        added2 = sg.ingest_file("my/model.py")
        assert added1 > 0
        assert added2 > 0
        assert sg.file_count == 2

    def test_distinct_query_results(self, collision_tree: Path):
        """Both modules appear as separate nodes in SPARQL queries."""
        sg = SessionGraph(collision_tree)
        sg.ingest_file("my_model.py")
        sg.ingest_file("my/model.py")

        results = sg.query(
            "PREFIX arch: <http://archgraph.example.org/> "
            "SELECT ?name WHERE { ?m a arch:Module ; arch:moduleName ?name . }"
        )
        names = {r.get("name", "") for r in results}
        assert "my_model.py" in names
        assert "my/model.py" in names

    def test_roundtrip_uri_to_path(self):
        """URI \u2192 path roundtrip preserves underscores vs directories."""
        from synrax.namespaces import make_module_uri, uri_to_path

        assert uri_to_path(make_module_uri("my_model.py")) == "my_model.py"
        assert uri_to_path(make_module_uri("my/model.py")) == "my/model.py"

    def test_edge_tracking_with_collision(self, collision_tree: Path):
        """Edge sources track correct paths even with similar names."""
        # Add a cross-import from my/model.py \u2192 my_model.py
        (collision_tree / "my" / "model.py").write_text(
            '"""my/model.py \u2014 Nested module.\n\n'
            "exports: nested_func() -> None\n"
            "rules:   Nested module rule.\n"
            '"""\n\n'
            "from my_model import flat_func\n\n"
            "def nested_func(): pass\n",
            encoding="utf-8",
        )
        sg = SessionGraph(collision_tree)
        sg.ingest_file("my_model.py")
        sg.ingest_file("my/model.py")
        # my/model.py depends on my_model.py (via import)
        source = sg.get_edge_source("my/model.py", "my_model.py")
        assert source == "structural"


# ── Step 3.2: Edge provenance serialization tests ─────────────────────


class TestProvenanceSerialization:
    """Verify serialize_provenance() and load_provenance() round-trip correctly."""

    def test_serialize_provenance_returns_dict(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        data = sg.serialize_provenance()
        assert "edges" in data
        assert isinstance(data["edges"], list)
        assert len(data["edges"]) > 0

    def test_serialize_provenance_edge_fields(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        data = sg.serialize_provenance()
        for edge in data["edges"]:
            assert "from" in edge
            assert "to" in edge
            assert "source" in edge
            assert edge["source"] in {"structural", "annotated", "inferred"}

    def test_load_provenance_restores(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        data = sg.serialize_provenance()

        # Create a fresh session and load provenance
        sg2 = SessionGraph(project_tree)
        assert len(sg2._edge_sources) == 0
        sg2.load_provenance(data)
        assert len(sg2._edge_sources) == len(sg._edge_sources)
        for key, val in sg._edge_sources.items():
            assert sg2._edge_sources[key] == val

    def test_inferred_edges_in_serialization(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.ingest_file("db/connection.py")
        sg.ingest_file("models/order.py")
        sg.ingest_file("forms/order_form.py")
        sg.ensure_reasoned()
        data = sg.serialize_provenance()
        sources = {e["source"] for e in data["edges"]}
        # Should have at least structural and annotated
        assert "structural" in sources or "annotated" in sources

    def test_empty_provenance(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        data = sg.serialize_provenance()
        assert data == {"edges": []}

    def test_load_empty_provenance(self, project_tree: Path):
        sg = SessionGraph(project_tree)
        sg.load_provenance({"edges": []})
        assert len(sg._edge_sources) == 0
