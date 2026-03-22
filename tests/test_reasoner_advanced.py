"""tests/test_reasoner_advanced.py — Extended OWL-RL reasoning tests."""

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, OWL, RDF, RDFS, bind_namespaces
from synrax.schema.reasoner import reason


def test_cascades_implies_used_by():
    """cascades is a subproperty of usedBy — reasoning should infer usedBy."""
    g = Graph()
    bind_namespaces(g)
    g.add((ARCH.A, RDF.type, ARCH.Module))
    g.add((ARCH.B, RDF.type, ARCH.Module))
    g.add((ARCH.A, ARCH.cascades, ARCH.B))

    g = reason(g)

    # cascades is rdfs:subPropertyOf usedBy → A usedBy B should be inferred
    assert (ARCH.A, ARCH.usedBy, ARCH.B) in g


def test_transitive_chain_three_hops():
    """A -> B -> C -> D: A should transitively depend on D after reasoning."""
    g = Graph()
    bind_namespaces(g)
    for name in ["A", "B", "C", "D"]:
        g.add((ARCH[name], RDF.type, ARCH.Module))
    g.add((ARCH.A, ARCH.dependsOn, ARCH.B))
    g.add((ARCH.B, ARCH.dependsOn, ARCH.C))
    g.add((ARCH.C, ARCH.dependsOn, ARCH.D))

    g = reason(g)

    assert (ARCH.A, ARCH.dependsOn, ARCH.D) in g
    assert (ARCH.A, ARCH.dependsOn, ARCH.C) in g
    assert (ARCH.B, ARCH.dependsOn, ARCH.D) in g


def test_inverse_used_by_from_depends_on():
    """dependsOn inverse is usedBy — both directions should exist after reasoning."""
    g = Graph()
    bind_namespaces(g)
    g.add((ARCH.X, RDF.type, ARCH.Module))
    g.add((ARCH.Y, RDF.type, ARCH.Module))
    g.add((ARCH.X, ARCH.dependsOn, ARCH.Y))

    g = reason(g)

    assert (ARCH.Y, ARCH.usedBy, ARCH.X) in g


def test_reasoning_preserves_original_triples():
    """Reasoning should not remove original triples."""
    g = Graph()
    bind_namespaces(g)
    g.add((ARCH.A, RDF.type, ARCH.Module))
    g.add((ARCH.A, ARCH.purpose, Literal("Test", datatype=XSD.string)))

    original_count = len(g)
    g = reason(g)

    # Should still have original triples plus inferred ones
    assert (ARCH.A, ARCH.purpose, Literal("Test", datatype=XSD.string)) in g
    assert len(g) >= original_count


def test_reasoning_returns_same_graph():
    """reason() should return the same graph object (in-place expansion)."""
    g = Graph()
    bind_namespaces(g)
    g.add((ARCH.A, RDF.type, ARCH.Module))

    result = reason(g)
    assert result is g


def test_reasoning_adds_schema_classes():
    """After reasoning, schema classes should be present in the graph."""
    g = Graph()
    bind_namespaces(g)
    g.add((ARCH.test, RDF.type, ARCH.Module))

    g = reason(g)

    # The schema defines Module as an owl:Class — this should be in the graph
    assert (ARCH.Module, RDF.type, OWL.Class) in g
