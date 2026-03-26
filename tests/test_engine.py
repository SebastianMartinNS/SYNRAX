"""tests/test_engine.py — Tests for SPARQL query engine execution."""

from pathlib import Path

import pytest
from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.query.engine import run_query

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def sample_turtle(tmp_path: Path) -> Path:
    """Create a Turtle file with a realistic dependency graph for query testing."""
    g = Graph()
    bind_namespaces(g)

    # Packages
    for pkg in ["api", "billing", "reports"]:
        uri = ARCH[f"proj_{pkg}"]
        g.add((uri, RDF.type, ARCH.Package))
        g.add((uri, ARCH.packageName, Literal(pkg, datatype=XSD.string)))
        g.add((uri, ARCH.purpose, Literal(f"{pkg} package", datatype=XSD.string)))

    # Modules
    billing_mod = ARCH["billing_invoice"]
    api_mod = ARCH["api_routes"]
    reports_mod = ARCH["reports_monthly"]

    for mod, name in [
        (billing_mod, "billing_invoice"),
        (api_mod, "api_routes"),
        (reports_mod, "reports_monthly"),
    ]:
        g.add((mod, RDF.type, ARCH.Module))
        g.add((mod, ARCH.moduleName, Literal(name, datatype=XSD.string)))
        g.add((mod, ARCH.purpose, Literal(f"Purpose of {name}", datatype=XSD.string)))

    # Dependencies: api -> billing -> reports (linear chain)
    g.add((api_mod, ARCH.dependsOn, billing_mod))
    g.add((billing_mod, ARCH.dependsOn, reports_mod))

    # Cascades
    g.add((reports_mod, ARCH.cascades, billing_mod))

    # Rules
    rule = ARCH["billing_invoice_rule_1"]
    g.add((rule, RDF.type, ARCH.Rule))
    g.add((rule, ARCH.content, Literal("Filter is_suspended before sum", datatype=XSD.string)))
    g.add((billing_mod, ARCH.hasRule, rule))

    # Agent session
    session = ARCH["session_2026_03_22"]
    agent = ARCH["agent_claude_opus_4"]
    g.add((session, RDF.type, ARCH.AgentSession))
    g.add((session, ARCH.sessionDate, Literal("2026-03-22", datatype=XSD.date)))
    g.add((session, ARCH.narrative, Literal("Initial implementation", datatype=XSD.string)))
    g.add((session, ARCH.belongs, agent))
    g.add((session, ARCH.visited, billing_mod))
    g.add((agent, RDF.type, ARCH.Agent))

    ttl = tmp_path / "test_graph.ttl"
    g.serialize(destination=str(ttl), format="turtle")
    return ttl


def test_run_query_impact_analysis(sample_turtle: Path):
    """Impact analysis should find modules that depend on a given module."""
    results = run_query("impact_analysis", sample_turtle, module="billing_invoice")
    names = [r.get("name", "") for r in results]
    assert "api_routes" in names


def test_run_query_unused_modules(sample_turtle: Path):
    """Unused modules should find modules nothing depends on."""
    results = run_query("unused_modules", sample_turtle)
    # reports_monthly is at the end of the chain — nothing depends on it
    # Wait, billing depends on reports. So let's check what's truly unused.
    # api_routes has nothing depending on it
    names = [r.get("name", "") for r in results]
    assert "api_routes" in names


def test_run_query_parameter_substitution(sample_turtle: Path):
    """Parameters should be substituted into query templates."""
    # impact_analysis uses {{module}} parameter
    results = run_query("impact_analysis", sample_turtle, module="reports_monthly")
    names = [r.get("name", "") for r in results]
    # billing depends on reports
    assert "billing_invoice" in names


def test_run_query_returns_list_of_dicts(sample_turtle: Path):
    results = run_query("unused_modules", sample_turtle)
    assert isinstance(results, list)
    for r in results:
        assert isinstance(r, dict)


def test_run_query_template_not_found(tmp_path: Path):
    ttl = tmp_path / "empty.ttl"
    g = Graph()
    g.serialize(destination=str(ttl), format="turtle")
    with pytest.raises(FileNotFoundError):
        run_query("nonexistent_template", ttl)
