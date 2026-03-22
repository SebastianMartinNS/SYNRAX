"""tests/test_module_parser.py — Tests for Python module docstring parser."""

from pathlib import Path

from synrax.extract.module_parser import parse_module
from synrax.namespaces import ARCH, RDF

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_module_creates_module():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 1


def test_parse_module_extracts_purpose():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    purposes = [str(o) for _, _, o in g.triples((None, ARCH.purpose, None))]
    assert any("Invoice generation" in p for p in purposes)


def test_parse_module_extracts_exports():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    exports = list(g.subjects(RDF.type, ARCH.Export))
    assert len(exports) >= 1
    names = {str(o) for _, _, o in g.triples((None, ARCH.exportName, None))}
    assert "build_invoice_total" in names


def test_parse_module_extracts_used_by():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    # used_by creates dependsOn triples (api/routes depends on this module)
    deps = list(g.triples((None, ARCH.dependsOn, None)))
    assert len(deps) >= 1


def test_parse_module_extracts_cascade():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    cascades = list(g.triples((None, ARCH.cascades, None)))
    assert len(cascades) >= 1


def test_parse_module_extracts_rules():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    rules = list(g.subjects(RDF.type, ARCH.Rule))
    assert len(rules) >= 2  # At least 2 module-level rules


def test_parse_module_extracts_agent_session():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    sessions = list(g.subjects(RDF.type, ARCH.AgentSession))
    assert len(sessions) >= 1


def test_parse_module_level2_function_rules():
    g = parse_module(FIXTURES / "billing" / "invoice_service.py")
    functions = list(g.subjects(RDF.type, ARCH.Function))
    assert len(functions) >= 1
