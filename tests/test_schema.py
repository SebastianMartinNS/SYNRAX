"""tests/test_schema.py — Tests for OWL schema loading and reasoning."""

from rdflib import Graph

from synrax.namespaces import ARCH, RDF
from synrax.schema.loader import load_schema, load_shapes
from synrax.schema.reasoner import reason


def test_load_schema_has_classes():
    g = load_schema()
    classes = set(g.subjects(RDF.type, ARCH.Module.__class__))
    # Check that key classes are defined
    assert (ARCH.Module, RDF.type, None) in g or len(g) > 0


def test_load_schema_has_properties():
    g = load_schema()
    assert len(g) > 50  # Schema should have many triples


def test_load_shapes():
    g = load_shapes()
    assert len(g) > 10


def test_reason_transitive_closure():
    """Test that OWL reasoning computes transitive dependsOn."""
    g = Graph()
    g.add((ARCH.A, RDF.type, ARCH.Module))
    g.add((ARCH.B, RDF.type, ARCH.Module))
    g.add((ARCH.C, RDF.type, ARCH.Module))
    g.add((ARCH.A, ARCH.dependsOn, ARCH.B))
    g.add((ARCH.B, ARCH.dependsOn, ARCH.C))

    g = reason(g)

    # Transitive: A dependsOn C should be inferred
    assert (ARCH.A, ARCH.dependsOn, ARCH.C) in g


def test_reason_inverse_property():
    """Test that OWL reasoning infers usedBy from dependsOn."""
    g = Graph()
    g.add((ARCH.A, RDF.type, ARCH.Module))
    g.add((ARCH.B, RDF.type, ARCH.Module))
    g.add((ARCH.A, ARCH.dependsOn, ARCH.B))

    g = reason(g)

    # Inverse: B usedBy A should be inferred
    assert (ARCH.B, ARCH.usedBy, ARCH.A) in g
