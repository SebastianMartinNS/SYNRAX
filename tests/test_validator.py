"""tests/test_validator.py — Tests for SHACL validation of ArchGraph RDF graphs."""

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.schema.validator import validate


def _make_valid_module(g: Graph, name: str = "billing_invoice") -> None:
    """Add a minimal valid Module to the graph (satisfies all shapes)."""
    uri = ARCH[name]
    g.add((uri, RDF.type, ARCH.Module))
    g.add((uri, ARCH.moduleName, Literal(name, datatype=XSD.string)))
    g.add((uri, ARCH.purpose, Literal("Test module purpose", datatype=XSD.string)))
    # Add a rule so RulePresenceShape warning doesn't fire
    rule_uri = ARCH[f"{name}_rule_1"]
    g.add((rule_uri, RDF.type, ARCH.Rule))
    g.add((rule_uri, ARCH.content, Literal("Must filter suspended", datatype=XSD.string)))
    g.add((uri, ARCH.hasRule, rule_uri))


def _make_valid_package(g: Graph, name: str = "billing") -> None:
    """Add a minimal valid Package to the graph."""
    uri = ARCH[name]
    g.add((uri, RDF.type, ARCH.Package))
    g.add((uri, ARCH.packageName, Literal(name, datatype=XSD.string)))
    g.add((uri, ARCH.purpose, Literal("Test package", datatype=XSD.string)))


def test_validate_empty_graph_conforms():
    """An empty graph has nothing to violate."""
    g = Graph()
    bind_namespaces(g)
    report = validate(g)
    assert report["conforms"] is True
    assert report["violations"] == []


def test_validate_valid_module_conforms():
    """A fully-annotated module should pass validation."""
    g = Graph()
    bind_namespaces(g)
    _make_valid_module(g)
    report = validate(g)
    assert report["conforms"] is True
    assert len(report["violations"]) == 0


def test_validate_module_missing_name_violates():
    """A module without moduleName should produce a violation."""
    g = Graph()
    bind_namespaces(g)
    uri = ARCH["bad_module"]
    g.add((uri, RDF.type, ARCH.Module))
    g.add((uri, ARCH.purpose, Literal("Has purpose but no name", datatype=XSD.string)))

    report = validate(g)
    assert report["conforms"] is False
    assert len(report["violations"]) > 0
    messages = [v.get("resultMessage", "") for v in report["violations"]]
    assert any("moduleName" in m for m in messages)


def test_validate_module_missing_purpose_violates():
    """A module without purpose should produce a violation."""
    g = Graph()
    bind_namespaces(g)
    uri = ARCH["bad_module"]
    g.add((uri, RDF.type, ARCH.Module))
    g.add((uri, ARCH.moduleName, Literal("bad_module", datatype=XSD.string)))

    report = validate(g)
    assert report["conforms"] is False


def test_validate_module_without_rules_warns():
    """A module with no rules should produce a warning (not a violation)."""
    g = Graph()
    bind_namespaces(g)
    uri = ARCH["norules"]
    g.add((uri, RDF.type, ARCH.Module))
    g.add((uri, ARCH.moduleName, Literal("norules", datatype=XSD.string)))
    g.add((uri, ARCH.purpose, Literal("Module without rules", datatype=XSD.string)))

    report = validate(g)
    # Should be a warning, not a hard violation (shape uses sh:Warning severity)
    assert len(report["warnings"]) > 0
    messages = [w.get("resultMessage", "") for w in report["warnings"]]
    assert any("rules" in m.lower() or "rule" in m.lower() for m in messages)


def test_validate_export_missing_name_violates():
    """An Export without exportName should fail validation."""
    g = Graph()
    bind_namespaces(g)
    _make_valid_module(g)
    export_uri = ARCH["bad_export"]
    g.add((export_uri, RDF.type, ARCH.Export))
    # No exportName added

    report = validate(g)
    assert report["conforms"] is False
    messages = [v.get("resultMessage", "") for v in report["violations"]]
    assert any("exportName" in m for m in messages)


def test_validate_package_missing_name_violates():
    """A Package without packageName should fail."""
    g = Graph()
    bind_namespaces(g)
    uri = ARCH["bad_pkg"]
    g.add((uri, RDF.type, ARCH.Package))
    g.add((uri, ARCH.purpose, Literal("Has purpose", datatype=XSD.string)))

    report = validate(g)
    assert report["conforms"] is False


def test_validate_report_has_statistics():
    """Report must contain statistics block with expected keys."""
    g = Graph()
    bind_namespaces(g)
    report = validate(g)
    assert "statistics" in report
    stats = report["statistics"]
    assert "violations_count" in stats
    assert "warnings_count" in stats
    assert "timestamp" in stats
    assert "validator_time_ms" in stats
    assert isinstance(stats["validator_time_ms"], int)


def test_validate_report_structure():
    """Report must have conforms, violations, warnings, statistics keys."""
    g = Graph()
    bind_namespaces(g)
    report = validate(g)
    assert set(report.keys()) == {"conforms", "violations", "warnings", "statistics"}


def test_validate_valid_package_conforms():
    """A fully-annotated package should pass validation."""
    g = Graph()
    bind_namespaces(g)
    _make_valid_package(g)
    report = validate(g)
    assert report["conforms"] is True


def test_package_with_deps_not_classified_as_module():
    """Regression: Packages using packageDependsOn must NOT be inferred as Module after reasoning.

    Previously, Packages used dependsOn (domain=Module), causing OWL-RL to classify
    them as Module, which triggered false SHACL violations (missing moduleName).
    With the fix, packageDependsOn has domain=Package so no type confusion occurs.
    """
    from synrax.schema.reasoner import reason

    g = Graph()
    bind_namespaces(g)

    # Create two packages with packageDependsOn
    pkg_a = ARCH["proj_billing"]
    pkg_b = ARCH["proj_api"]
    g.add((pkg_a, RDF.type, ARCH.Package))
    g.add((pkg_a, ARCH.packageName, Literal("billing/", datatype=XSD.string)))
    g.add((pkg_a, ARCH.purpose, Literal("Billing package", datatype=XSD.string)))
    g.add((pkg_b, RDF.type, ARCH.Package))
    g.add((pkg_b, ARCH.packageName, Literal("api/", datatype=XSD.string)))
    g.add((pkg_b, ARCH.purpose, Literal("API package", datatype=XSD.string)))
    g.add((pkg_a, ARCH.packageDependsOn, pkg_b))

    # Apply OWL-RL reasoning
    reason(g)

    # Packages must NOT be classified as Module
    modules = {s for s, _, _ in g.triples((None, RDF.type, ARCH.Module))}
    assert pkg_a not in modules, "Package pkg_a was incorrectly classified as Module"
    assert pkg_b not in modules, "Package pkg_b was incorrectly classified as Module"

    # SHACL validation should pass (no false ModuleCompletenessShape violations)
    report = validate(g)
    # Filter violations to only those on our package URIs
    pkg_violations = [
        v for v in report["violations"]
        if "proj_billing" in v.get("focusNode", "") or "proj_api" in v.get("focusNode", "")
    ]
    assert len(pkg_violations) == 0, f"Package false positives: {pkg_violations}"
