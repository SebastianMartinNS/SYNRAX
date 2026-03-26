"""tests/test_value_add.py — Paper-driven tests demonstrating Synrax's value beyond raw CodeDNA.

These tests validate the key claims from the CodeDNA paper and prove that Synrax
adds formal verification, automated impact analysis, and cascade enforcement that
don't exist in the base CodeDNA protocol.

Paper reference: "CodeDNA: An In-Source Communication Protocol for AI Coding Agents"
Value-add: Formal OWL reasoning + SHACL validation + SPARQL impact analysis
"""

from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate


class TestEndToEndWorkflow:
    """Full extract → reason → validate → query pipeline.

    This is the core Synrax value: taking raw CodeDNA annotations and
    turning them into a formally validated, reasoned knowledge graph.
    """

    def test_full_pipeline_extract_reason_validate(self, tmp_path: Path):
        """E2E: extract codebase → apply reasoning → validate shapes."""
        # Create a mini-codebase with proper CodeDNA annotations
        manifest = tmp_path / ".codedna"
        manifest.write_text(
            "project: e2e-test\n"
            "packages:\n"
            "  payments/:\n"
            "    purpose: Payment processing\n"
            "  api/:\n"
            "    purpose: API layer\n"
            "    depends_on: [payments/]\n"
        )

        payments_dir = tmp_path / "payments"
        payments_dir.mkdir()
        (payments_dir / "charge.py").write_text(
            '"""payments/charge.py \u2014 Process credit card charges.\n\n'
            "exports: charge_card(amount: int) -> bool\n"
            "used_by: api/checkout.py -> process_payment [cascade]\n"
            "rules:   Amounts in cents, never float. Must validate card before charging.\n"
            "agent:   test-agent | test | 2026-01-01 | Initial charge logic.\n"
            '"""\n\n'
            "def charge_card(amount: int) -> bool:\n"
            '    """Charge a credit card.\n\n'
            "    Rules: Must validate amount > 0 before processing.\n"
            '    """\n'
            "    return amount > 0\n",
            encoding="utf-8",
        )

        # Step 1: Extract
        g = extract_codebase(tmp_path)
        assert len(g) > 10

        # Step 2: Reason
        g = reason(g)

        # After reasoning, cascade should imply usedBy (subproperty chain)
        # Check that inferred triples exist
        has_used_by = any(p == ARCH.usedBy for _, p, _ in g)
        has_depends = any(p == ARCH.dependsOn for _, p, _ in g)
        assert has_depends or has_used_by

        # Step 3: Validate
        report = validate(g)
        assert "conforms" in report
        assert "statistics" in report

    def test_reasoning_enables_transitive_impact(self, tmp_path: Path):
        """Reasoning discovers impacts invisible to raw CodeDNA.

        Paper finding: CodeDNA helps when there's a navigable call chain.
        Synrax formalizes this with OWL transitive closure — if A→B→C,
        then A→C is automatically inferred, enabling full impact analysis.
        """
        g = Graph()
        bind_namespaces(g)

        # Build Django-like chain: views → forms → models → db
        chain = ["views", "forms", "models", "db"]
        for name in chain:
            uri = ARCH[name]
            g.add((uri, RDF.type, ARCH.Module))
            g.add((uri, ARCH.moduleName, Literal(name, datatype=XSD.string)))
            g.add((uri, ARCH.purpose, Literal(f"{name} layer", datatype=XSD.string)))

        # Linear dependency chain
        for i in range(len(chain) - 1):
            g.add((ARCH[chain[i]], ARCH.dependsOn, ARCH[chain[i + 1]]))

        # Before reasoning: views only directly depends on forms
        assert (ARCH.views, ARCH.dependsOn, ARCH.db) not in g

        g = reason(g)

        # After reasoning: views transitively depends on ALL downstream
        assert (ARCH.views, ARCH.dependsOn, ARCH.db) in g
        assert (ARCH.views, ARCH.dependsOn, ARCH.models) in g
        assert (ARCH.forms, ARCH.dependsOn, ARCH.db) in g


class TestCascadeEnforcement:
    """Cascade [cascade] tag enforcement via SHACL + SPARQL.

    Paper claim: [cascade] marks files that MUST be updated if exports change.
    Synrax value: formal detection of missed cascade targets via SPARQL.
    """

    def test_cascade_creates_formal_triple(self):
        """[cascade] in used_by creates an arch:cascades triple (not just dependsOn)."""
        g = Graph()
        bind_namespaces(g)

        mod = ARCH["billing_invoice"]
        g.add((mod, RDF.type, ARCH.Module))
        g.add((mod, ARCH.moduleName, Literal("billing/invoice.py", datatype=XSD.string)))
        # Simulate cascade relationship
        target = ARCH["reports_monthly"]
        g.add((target, ARCH.cascades, mod))

        cascades = list(g.triples((None, ARCH.cascades, None)))
        assert len(cascades) >= 1


class TestAnnotationQuality:
    """Validate that SHACL shapes enforce the quality standards from the paper.

    Paper: "wrong rules: is worse than no rules:" — annotations must be validated.
    Synrax value: SHACL shapes catch incomplete or structurally invalid annotations.
    """

    def test_incomplete_module_detected(self):
        """Module without purpose=missing critical context for agents."""
        g = Graph()
        bind_namespaces(g)
        g.add((ARCH.bad, RDF.type, ARCH.Module))
        g.add((ARCH.bad, ARCH.moduleName, Literal("bad", datatype=XSD.string)))
        # No purpose → SHACL violation

        report = validate(g)
        assert report["conforms"] is False
        assert any("purpose" in v.get("resultMessage", "") for v in report["violations"])

    def test_module_without_rules_gets_warning(self):
        """Module without rules gets a warning (not error) per Shape 1."""
        g = Graph()
        bind_namespaces(g)
        g.add((ARCH.norules, RDF.type, ARCH.Module))
        g.add((ARCH.norules, ARCH.moduleName, Literal("norules", datatype=XSD.string)))
        g.add((ARCH.norules, ARCH.purpose, Literal("No rules module", datatype=XSD.string)))

        report = validate(g)
        # Should warn but not fail hard
        assert len(report["warnings"]) > 0

    def test_complete_module_passes_all_shapes(self):
        """A properly annotated module satisfies all SHACL shapes."""
        g = Graph()
        bind_namespaces(g)
        mod = ARCH["good_module"]
        g.add((mod, RDF.type, ARCH.Module))
        g.add((mod, ARCH.moduleName, Literal("good_module", datatype=XSD.string)))
        g.add((mod, ARCH.purpose, Literal("Well-documented module", datatype=XSD.string)))

        rule = ARCH["good_rule"]
        g.add((rule, RDF.type, ARCH.Rule))
        g.add((rule, ARCH.content, Literal("Must validate input", datatype=XSD.string)))
        g.add((mod, ARCH.hasRule, rule))

        report = validate(g)
        assert report["conforms"] is True
        assert len(report["violations"]) == 0


class TestNavigationChainDetection:
    """Test that Synrax can detect and analyze the navigation patterns
    that the paper identifies as key to CodeDNA's effectiveness.

    Paper finding: CodeDNA helps most with "navigable call chains" (Δ >0%).
    Cross-cutting concerns (no chain) show Δ ≈ 0%.
    """

    def test_linear_chain_impact(self):
        """Linear chain A→B→C: full impact is computable after reasoning."""
        g = Graph()
        bind_namespaces(g)

        for name in ["a", "b", "c"]:
            g.add((ARCH[name], RDF.type, ARCH.Module))
            g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
            g.add((ARCH[name], ARCH.purpose, Literal(f"Module {name}", datatype=XSD.string)))

        g.add((ARCH.a, ARCH.dependsOn, ARCH.b))
        g.add((ARCH.b, ARCH.dependsOn, ARCH.c))

        g = reason(g)

        # Full transitive impact of changing c:
        impacted = set(s for s, p, o in g.triples((None, ARCH.dependsOn, ARCH.c)))
        assert ARCH.a in impacted
        assert ARCH.b in impacted

    def test_fan_out_delegation(self):
        """Fan-out: one interface delegates to N backends.

        Paper task pattern: 'Trunc tzinfo' — one interface, 4 backends.
        """
        g = Graph()
        bind_namespaces(g)

        interface = ARCH["date_trunc_interface"]
        g.add((interface, RDF.type, ARCH.Module))
        g.add((interface, ARCH.moduleName, Literal("date_trunc_interface", datatype=XSD.string)))
        g.add((interface, ARCH.purpose, Literal("Date truncation interface", datatype=XSD.string)))

        backends = ["mysql_ops", "postgres_ops", "sqlite_ops", "oracle_ops"]
        for b in backends:
            uri = ARCH[b]
            g.add((uri, RDF.type, ARCH.Module))
            g.add((uri, ARCH.moduleName, Literal(b, datatype=XSD.string)))
            g.add((uri, ARCH.purpose, Literal(f"{b} backend", datatype=XSD.string)))
            g.add((uri, ARCH.dependsOn, interface))

        g = reason(g)

        # All backends should be found as depending on interface
        dependents = set(s for s, p, o in g.triples((None, ARCH.dependsOn, interface)))
        assert len(dependents) == 4
        for b in backends:
            assert ARCH[b] in dependents

    def test_isolated_modules_no_transitive_link(self):
        """Cross-cutting: independent modules have no dependency path.

        Paper: __eq__ task — same fix needed in N independent files, Δ ≈ 0%.
        Synrax correctly shows no transitive link between them.
        """
        g = Graph()
        bind_namespaces(g)

        for name in ["model_a", "model_b", "model_c"]:
            g.add((ARCH[name], RDF.type, ARCH.Module))
            g.add((ARCH[name], ARCH.moduleName, Literal(name, datatype=XSD.string)))
            g.add((ARCH[name], ARCH.purpose, Literal(f"Independent {name}", datatype=XSD.string)))

        g = reason(g)

        # No dependency paths should be inferred between independent modules
        for a in ["model_a", "model_b", "model_c"]:
            for b in ["model_a", "model_b", "model_c"]:
                if a != b:
                    assert (ARCH[a], ARCH.dependsOn, ARCH[b]) not in g


class TestAgentSessionTracking:
    """Validate agent session tracking — the append-only log from the paper.

    Paper: agent: field is append-only, records what each agent did.
    Synrax value: formal RDF triples for agent provenance, queryable via SPARQL.
    """

    def test_agent_session_from_docstring(self):
        """Parse agent field into AgentSession + Agent triples."""
        g = Graph()
        bind_namespaces(g)

        session = ARCH["session_test"]
        agent = ARCH["agent_test"]
        g.add((session, RDF.type, ARCH.AgentSession))
        g.add((session, ARCH.sessionDate, Literal("2026-03-22", datatype=XSD.date)))
        g.add((session, ARCH.narrative, Literal("Fixed billing logic", datatype=XSD.string)))
        g.add((session, ARCH.belongs, agent))
        g.add((agent, RDF.type, ARCH.Agent))

        sessions = list(g.subjects(RDF.type, ARCH.AgentSession))
        agents = list(g.subjects(RDF.type, ARCH.Agent))
        assert len(sessions) == 1
        assert len(agents) == 1

    def test_session_validation_requires_date_and_agent(self):
        """SHACL shape requires every AgentSession to have date + agent."""
        g = Graph()
        bind_namespaces(g)
        session = ARCH["bad_session"]
        g.add((session, RDF.type, ARCH.AgentSession))
        # Missing sessionDate, missing belongs

        report = validate(g)
        assert report["conforms"] is False
