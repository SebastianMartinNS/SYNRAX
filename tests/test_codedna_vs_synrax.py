"""tests/test_codedna_vs_synrax.py — 10 quantitative comparison tests:
raw CodeDNA (text-only, no reasoning, no validation, no SPARQL) vs
Synrax-enhanced output (OWL reasoning + SHACL validation + SPARQL queries).

Paper reference: "CodeDNA: An In-Source Communication Protocol for AI Coding Agents"
Each test measures a specific before/after metric with concrete numbers.
"""

import time
from pathlib import Path

import pytest
from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.query.engine import run_query
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate


# ---------------------------------------------------------------------------
# Shared fixture: realistic 5-module codebase with CodeDNA annotations
# ---------------------------------------------------------------------------

@pytest.fixture()
def realistic_codebase(tmp_path: Path):
    """Build a realistic codebase with 4 chained packages + 1 orphan.

    Returns (raw_graph, reasoned_graph, tmp_path).
    """
    # .codedna manifest — 5 packages, chain: views→forms→models→db, orphan: utils
    manifest = tmp_path / ".codedna"
    manifest.write_text(
        "project: comparison-test\n"
        "packages:\n"
        "  views/:\n"
        "    purpose: HTTP request handlers\n"
        "    depends_on: [forms/]\n"
        "  forms/:\n"
        "    purpose: Input validation logic\n"
        "    depends_on: [models/]\n"
        "  models/:\n"
        "    purpose: ORM data layer\n"
        "    depends_on: [db/]\n"
        "  db/:\n"
        "    purpose: Database connection pool\n"
        "  utils/:\n"
        "    purpose: Miscellaneous helpers\n",
        encoding="utf-8",
    )

    # --- views/checkout.py (complete, with cascade) ---
    views_dir = tmp_path / "views"
    views_dir.mkdir()
    (views_dir / "checkout.py").write_text(
        '"""views/checkout.py \u2014 Checkout HTTP handler.\n\n'
        "exports: checkout_view(request) -> HttpResponse\n"
        "used_by: urls.py -> urlpatterns\n"
        "rules:   Must validate CSRF token. Never trust client-side totals.\n"
        "agent:   test-model | test-provider | 2026-01-15 | Wired checkout flow.\n"
        '"""\n\n'
        "def checkout_view(request):\n"
        '    """Process checkout.\n\n'
        "    Rules: Validate cart is not empty before processing.\n"
        '    """\n'
        "    return None\n",
        encoding="utf-8",
    )

    # --- forms/order_form.py (complete, has cascade tag) ---
    forms_dir = tmp_path / "forms"
    forms_dir.mkdir()
    (forms_dir / "order_form.py").write_text(
        '"""forms/order_form.py \u2014 Order validation.\n\n'
        "exports: validate_order(data: dict) -> bool, build_line_items(cart) -> list\n"
        "used_by: views/checkout.py -> checkout_view [cascade], notifications/email.py -> send_confirmation\n"
        "rules:   Quantities must be positive integers. Reject negative totals.\n"
        "agent:   test-model | test-provider | 2026-02-10 | Added line item builder.\n"
        '"""\n\n'
        "def validate_order(data: dict) -> bool:\n"
        '    """Validate an order.\n\n'
        "    Rules: Total must match sum of line items.\n"
        '    """\n'
        "    return True\n\n"
        "def build_line_items(cart) -> list:\n"
        '    """Build line items from cart."""\n'
        "    return []\n",
        encoding="utf-8",
    )

    # --- models/order.py (complete) ---
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    (models_dir / "order.py").write_text(
        '"""models/order.py \u2014 Order ORM model.\n\n'
        "exports: Order(Model)\n"
        "used_by: forms/order_form.py -> validate_order\n"
        "rules:   PK is UUID. Soft-delete only, never hard delete.\n"
        "agent:   test-model | test-provider | 2026-01-05 | Initial order model.\n"
        '"""\n\n'
        "class Order:\n"
        "    pass\n",
        encoding="utf-8",
    )

    # --- db/connection.py (complete) ---
    db_dir = tmp_path / "db"
    db_dir.mkdir()
    (db_dir / "connection.py").write_text(
        '"""db/connection.py \u2014 Database connection pool.\n\n'
        "exports: get_pool() -> ConnectionPool\n"
        "used_by: models/order.py -> Order\n"
        "rules:   Max 20 connections. Timeout after 30s.\n"
        "agent:   test-model | test-provider | 2026-01-01 | Initial pool.\n"
        '"""\n\n'
        "def get_pool():\n"
        '    """Get connection pool.\n\n'
        "    Rules: Recycle connections older than 1 hour.\n"
        '    """\n'
        "    return None\n",
        encoding="utf-8",
    )

    # --- utils/helpers.py (orphan — no one depends on it) ---
    utils_dir = tmp_path / "utils"
    utils_dir.mkdir()
    (utils_dir / "helpers.py").write_text(
        '"""utils/helpers.py \u2014 Miscellaneous helpers.\n\n'
        "exports: slugify(text: str) -> str\n"
        "rules:   Pure functions only. No side effects.\n"
        "agent:   test-model | test-provider | 2026-03-01 | Added slugify.\n"
        '"""\n\n'
        "def slugify(text: str) -> str:\n"
        '    """Slugify text.\n\n'
        "    Rules: Must handle unicode correctly.\n"
        '    """\n'
        '    return text.lower().replace(" ", "-")\n',
        encoding="utf-8",
    )

    raw_graph = extract_codebase(tmp_path)
    reasoned_graph = extract_codebase(tmp_path)
    reason(reasoned_graph)

    return raw_graph, reasoned_graph, tmp_path


# ---------------------------------------------------------------------------
# Helper: build a simple module graph in-memory
# ---------------------------------------------------------------------------

def _make_chain(names: list[str]) -> Graph:
    """Build a linear dependency chain: names[0]→names[1]→…→names[-1]."""
    g = Graph()
    bind_namespaces(g)
    for name in names:
        g.add((ARCH[name], RDF.type, ARCH.Module))
        g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
        g.add((ARCH[name], ARCH.purpose, Literal(f"Module {name}", datatype=XSD.string)))
    for i in range(len(names) - 1):
        g.add((ARCH[names[i]], ARCH.dependsOn, ARCH[names[i + 1]]))
    return g


def _make_independent(names: list[str]) -> Graph:
    """Build independent (disconnected) modules with no edges."""
    g = Graph()
    bind_namespaces(g)
    for name in names:
        g.add((ARCH[name], RDF.type, ARCH.Module))
        g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
        g.add((ARCH[name], ARCH.purpose, Literal(f"Module {name}", datatype=XSD.string)))
    return g


# ===========================================================================
# TEST CLASS: 10 quantitative comparison tests
# ===========================================================================


class TestCodeDNAvsSynrax:
    """10 tests that measure how Synrax improves over raw CodeDNA.

    Each test documents:
      - CodeDNA limitation (the "before")
      - Synrax capability (the "after")
      - Concrete metric (number or boolean)
    """

    # ------------------------------------------------------------------
    # 1. Knowledge amplification: triple expansion ratio
    # ------------------------------------------------------------------

    def test_knowledge_amplification(self, realistic_codebase):
        """OWL reasoning amplifies raw triples by >100%.

        CodeDNA: produces only explicitly stated triples.
        Synrax:  OWL-RL reasoning infers transitive deps, inverse
                 properties, subproperty propagation → >2× the triples.
        """
        raw_graph, reasoned_graph, _ = realistic_codebase
        raw_count = len(raw_graph)
        reasoned_count = len(reasoned_graph)
        inferred = reasoned_count - raw_count

        assert reasoned_count > raw_count * 2, (
            f"Expected >2× amplification, got {reasoned_count}/{raw_count} "
            f"= {reasoned_count / raw_count:.1f}×"
        )
        assert inferred >= 50, (
            f"Expected ≥50 inferred triples, got {inferred}"
        )

    # ------------------------------------------------------------------
    # 2. Transitive depth discovery: dependency reach per node
    # ------------------------------------------------------------------

    def test_transitive_depth_discovery(self):
        """OWL reasoning expands dependency reach from 1 hop to N hops.

        CodeDNA: A→B is stated; A has no knowledge of C, D, E.
        Synrax:  After reasoning, A→B, A→C, A→D, A→E are all present.
        Metric:  Reach of A goes from 1 to 4.
        """
        g = _make_chain(["A", "B", "C", "D", "E"])

        # Before reasoning: A reaches only B
        before = set(o for _, _, o in g.triples((ARCH.A, ARCH.dependsOn, None)))
        assert len(before) == 1, f"Before reasoning A should reach 1, got {len(before)}"

        reason(g)

        # After reasoning: A reaches B, C, D, E
        after = set(o for _, _, o in g.triples((ARCH.A, ARCH.dependsOn, None)))
        assert len(after) == 4, f"After reasoning A should reach 4, got {len(after)}"
        assert {ARCH.B, ARCH.C, ARCH.D, ARCH.E} == after

    # ------------------------------------------------------------------
    # 3. Inverse relation generation: usedBy from dependsOn
    # ------------------------------------------------------------------

    def test_inverse_relation_generation(self, realistic_codebase):
        """OWL reasoning auto-generates usedBy (inverse of dependsOn).

        CodeDNA: no reverse perspective — you only know who A depends on,
                 not who depends on A.
        Synrax:  Every dependsOn edge generates a corresponding usedBy edge.
        Metric:  usedBy count goes from 0 to ≥4.
        """
        raw_graph, reasoned_graph, _ = realistic_codebase

        raw_used_by = list(raw_graph.triples((None, ARCH.usedBy, None)))
        reasoned_used_by = list(reasoned_graph.triples((None, ARCH.usedBy, None)))

        assert len(raw_used_by) == 0, (
            f"Raw graph should have 0 usedBy triples, got {len(raw_used_by)}"
        )
        assert len(reasoned_used_by) >= 4, (
            f"Reasoned graph should have ≥4 usedBy triples, got {len(reasoned_used_by)}"
        )

    # ------------------------------------------------------------------
    # 4. Multi-defect detection: SHACL catches 5 intentional defects
    # ------------------------------------------------------------------

    def test_multi_defect_detection(self):
        """SHACL validation catches all structural defects at once.

        CodeDNA: no validation mechanism — incomplete annotations are silent.
        Synrax:  SHACL shapes catch missing fields, wrong types, absent rules.
        Metric:  5 intentional defects → ≥4 violations + ≥1 warning.
        """
        g = Graph()
        bind_namespaces(g)

        # Defect 1: Module without moduleName
        g.add((ARCH.d1, RDF.type, ARCH.Module))
        g.add((ARCH.d1, ARCH.purpose, Literal("Has purpose no name", datatype=XSD.string)))

        # Defect 2: Module without purpose
        g.add((ARCH.d2, RDF.type, ARCH.Module))
        g.add((ARCH.d2, ARCH.moduleName, Literal("d2", datatype=XSD.string)))

        # Defect 3: Module without rules (warning, not error)
        g.add((ARCH.d3, RDF.type, ARCH.Module))
        g.add((ARCH.d3, ARCH.moduleName, Literal("d3", datatype=XSD.string)))
        g.add((ARCH.d3, ARCH.purpose, Literal("No rules", datatype=XSD.string)))

        # Defect 4: Export without exportName
        g.add((ARCH.d4, RDF.type, ARCH.Export))

        # Defect 5: Package without packageName
        g.add((ARCH.d5, RDF.type, ARCH.Package))
        g.add((ARCH.d5, ARCH.purpose, Literal("Has purpose", datatype=XSD.string)))

        report = validate(g)

        assert report["conforms"] is False
        assert len(report["violations"]) >= 4, (
            f"Expected ≥4 violations, got {len(report['violations'])}"
        )
        assert len(report["warnings"]) >= 1, (
            f"Expected ≥1 warning, got {len(report['warnings'])}"
        )

        # Each defect should produce a unique message keyword
        all_messages = " ".join(
            v.get("resultMessage", "") for v in report["violations"]
        )
        assert "moduleName" in all_messages, "Missing moduleName defect not caught"
        assert "purpose" in all_messages, "Missing purpose defect not caught"
        assert "exportName" in all_messages, "Missing exportName defect not caught"
        assert "packageName" in all_messages, "Missing packageName defect not caught"

    # ------------------------------------------------------------------
    # 5. Blast radius accuracy: direct vs transitive impact count
    # ------------------------------------------------------------------

    def test_blast_radius_accuracy(self, tmp_path: Path):
        """SPARQL impact analysis: reasoning triples the blast radius.

        CodeDNA: impact analysis requires manually opening every file.
        Synrax:  One SPARQL query, and after reasoning it shows ALL
                 transitive dependents — not just direct ones.
        Metric:  Direct dependents of 'db': 1.  After reasoning: 3.
        """
        g = _make_chain(["views", "forms", "models", "db"])

        # Save raw graph and query
        raw_ttl = tmp_path / "raw_blast.ttl"
        g.serialize(destination=str(raw_ttl), format="turtle")
        raw_results = run_query("impact_analysis", raw_ttl, module="db")

        # Apply reasoning and query again
        reason(g)
        reasoned_ttl = tmp_path / "reasoned_blast.ttl"
        g.serialize(destination=str(reasoned_ttl), format="turtle")
        reasoned_results = run_query("impact_analysis", reasoned_ttl, module="db")

        raw_count = len(raw_results)
        reasoned_count = len(reasoned_results)

        assert raw_count == 1, (
            f"Raw impact of 'db' should be 1 (only models), got {raw_count}"
        )
        assert reasoned_count == 3, (
            f"Reasoned impact of 'db' should be 3 (models+forms+views), "
            f"got {reasoned_count}"
        )

    # ------------------------------------------------------------------
    # 6. Cascade violation enforcement
    # ------------------------------------------------------------------

    def test_cascade_violation_enforcement(self, tmp_path: Path):
        """SPARQL detects when an agent skips a [cascade] target.

        CodeDNA: [cascade] is a text hint — no way to enforce it.
        Synrax:  cascade_violations SPARQL query formally detects missed targets.
        Metric:  1 cascade violation detected for the skipped target.
        """
        g = Graph()
        bind_namespaces(g)

        # Two modules, A cascades to B
        for name in ["mod_src", "mod_target"]:
            g.add((ARCH[name], RDF.type, ARCH.Module))
            g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
            g.add((ARCH[name], ARCH.purpose, Literal(f"Purpose of {name}", datatype=XSD.string)))

        g.add((ARCH.mod_src, ARCH.cascades, ARCH.mod_target))

        # Agent session: visited mod_src but NOT mod_target
        session = ARCH["test_session"]
        agent = ARCH["test_agent"]
        g.add((session, RDF.type, ARCH.AgentSession))
        g.add((session, ARCH.sessionDate, Literal("2026-03-22", datatype=XSD.date)))
        g.add((session, ARCH.narrative, Literal("Edited source only", datatype=XSD.string)))
        g.add((session, ARCH.belongs, agent))
        g.add((session, ARCH.visited, ARCH.mod_src))
        g.add((agent, RDF.type, ARCH.Agent))

        ttl = tmp_path / "cascade.ttl"
        g.serialize(destination=str(ttl), format="turtle")

        results = run_query("cascade_violations", ttl)
        assert len(results) >= 1, "Should detect at least 1 cascade violation"

    # ------------------------------------------------------------------
    # 7. Circular dependency detection
    # ------------------------------------------------------------------

    def test_circular_dependency_detection(self, tmp_path: Path):
        """SPARQL detects circular dependencies invisible to CodeDNA.

        CodeDNA: no cycle detection — circular deps silently exist in text.
        Synrax:  circular_deps SPARQL query uses property paths to find cycles.
        Metric:  ≥1 cycle detected in a 3-node cycle X→Y→Z→X.
        """
        g = Graph()
        bind_namespaces(g)

        for name in ["x", "y", "z"]:
            g.add((ARCH[name], RDF.type, ARCH.Module))
            g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
            g.add((ARCH[name], ARCH.purpose, Literal(f"Module {name}", datatype=XSD.string)))

        # Cycle: x→y→z→x
        g.add((ARCH.x, ARCH.dependsOn, ARCH.y))
        g.add((ARCH.y, ARCH.dependsOn, ARCH.z))
        g.add((ARCH.z, ARCH.dependsOn, ARCH.x))

        # Reason to compute transitive closure (circular_deps.rq runs on reasoned graphs)
        reason(g)

        ttl = tmp_path / "circular.ttl"
        g.serialize(destination=str(ttl), format="turtle")

        results = run_query("circular_deps", ttl)
        assert len(results) >= 1, "Should detect at least 1 circular dependency"

    # ------------------------------------------------------------------
    # 8. Orphan module identification
    # ------------------------------------------------------------------

    def test_orphan_module_identification(self, tmp_path: Path):
        """SPARQL identifies orphan modules invisible to CodeDNA.

        CodeDNA: no way to surface which modules nobody depends on.
        Synrax:  unused_modules SPARQL query finds them in one shot.
        Metric:  True orphan (no deps in or out) is detected;
                 depended-upon modules in the chain are NOT flagged.
        """
        g = _make_chain(["conn_a", "conn_b", "conn_c"])

        # Add a true orphan — no one depends on it AND it depends on nothing
        g.add((ARCH.orphan_d, RDF.type, ARCH.Module))
        g.add((ARCH.orphan_d, ARCH.moduleName, Literal("orphan_d", datatype=XSD.string)))
        g.add((ARCH.orphan_d, ARCH.purpose, Literal("Forgotten module", datatype=XSD.string)))

        ttl = tmp_path / "orphan.ttl"
        g.serialize(destination=str(ttl), format="turtle")

        results = run_query("unused_modules", ttl)
        names = [r.get("name", "") for r in results]

        assert "orphan_d" in names, f"Orphan D not found, got {names}"
        # Modules that are depended-upon (conn_b, conn_c) should NOT be orphans
        for depended_upon in ["conn_b", "conn_c"]:
            assert depended_upon not in names, f"{depended_upon} is depended-upon, should not be an orphan"

    # ------------------------------------------------------------------
    # 9. Full pipeline performance
    # ------------------------------------------------------------------

    def test_full_pipeline_performance(self, tmp_path: Path):
        """Full Synrax pipeline (extract→reason→validate→query) runs in <10s.

        CodeDNA: text-only, no pipeline exists.
        Synrax:  complete formal pipeline from source to queryable graph.
        Metric:  wall-clock time < 10s; all outputs structurally valid.
        """
        # Reuse the realistic codebase fixture inline for timing accuracy
        manifest = tmp_path / ".codedna"
        manifest.write_text(
            "project: perf-test\n"
            "packages:\n"
            "  svc/:\n"
            "    purpose: Service layer\n"
            "  repo/:\n"
            "    purpose: Repository layer\n"
            "    depends_on: [svc/]\n",
            encoding="utf-8",
        )

        svc_dir = tmp_path / "svc"
        svc_dir.mkdir()
        (svc_dir / "handler.py").write_text(
            '"""svc/handler.py \u2014 Service handler.\n\n'
            "exports: handle(req) -> Response\n"
            "rules:   Timeout after 5s.\n"
            "agent:   model | provider | 2026-01-01 | Initial.\n"
            '"""\n\ndef handle(req): return None\n',
            encoding="utf-8",
        )

        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        (repo_dir / "store.py").write_text(
            '"""repo/store.py \u2014 Data store.\n\n'
            "exports: save(item) -> bool\n"
            "used_by: svc/handler.py -> handle\n"
            "rules:   Must use transactions.\n"
            "agent:   model | provider | 2026-01-01 | Initial.\n"
            '"""\n\ndef save(item): return True\n',
            encoding="utf-8",
        )

        start = time.monotonic()

        # Step 1: Extract
        graph = extract_codebase(tmp_path)
        assert len(graph) > 0

        # Step 2: Reason
        graph = reason(graph)
        assert len(graph) > 0

        # Step 3: Validate
        report = validate(graph)
        assert "conforms" in report
        assert "statistics" in report

        # Step 4: SPARQL query
        ttl = tmp_path / "perf.ttl"
        graph.serialize(destination=str(ttl), format="turtle")
        results = run_query("unused_modules", ttl)
        assert isinstance(results, list)

        elapsed = time.monotonic() - start
        assert elapsed < 10.0, f"Pipeline took {elapsed:.1f}s, expected <10s"

    # ------------------------------------------------------------------
    # 10. Navigable chain vs cross-cutting topology (paper's key finding)
    # ------------------------------------------------------------------

    def test_navigable_chain_vs_crosscutting_topology(self):
        """Reasoning adds edges only where navigable chains exist.

        Paper finding: CodeDNA helps most with navigable call chains (Δ>0%).
        Cross-cutting concerns with no chain show Δ≈0%.
        Synrax formally confirms this: chain graphs gain new edges,
        independent graphs gain zero.

        Metric:
          Chain (A→B→C→D):   ≥3 new dependsOn edges after reasoning
          Independent (W,X,Y,Z): 0 new dependsOn edges after reasoning
        """
        # --- Chain topology ---
        chain_g = _make_chain(["ch_a", "ch_b", "ch_c", "ch_d"])
        chain_before = set(chain_g.triples((None, ARCH.dependsOn, None)))

        reason(chain_g)
        chain_after = set(chain_g.triples((None, ARCH.dependsOn, None)))
        chain_new = len(chain_after) - len(chain_before)

        # --- Independent topology ---
        indep_g = _make_independent(["ind_w", "ind_x", "ind_y", "ind_z"])
        indep_before = set(indep_g.triples((None, ARCH.dependsOn, None)))

        reason(indep_g)
        indep_after = set(indep_g.triples((None, ARCH.dependsOn, None)))
        indep_new = len(indep_after) - len(indep_before)

        assert chain_new >= 3, (
            f"Chain should gain ≥3 new dependsOn edges, got {chain_new}"
        )
        assert indep_new == 0, (
            f"Independent modules should gain 0 new dependsOn edges, got {indep_new}"
        )
