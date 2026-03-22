"""synrax/schema/reasoner.py — OWL-RL reasoning over ArchGraph triples.

exports: reason(graph) -> Graph
used_by: synrax/cli/main.py → export command | synrax/schema/__init__.py
rules:   Uses owlrl for OWL-RL entailment (transitive closure, inverse properties, subclass propagation).
         Merges schema.owl axioms into the graph before reasoning.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial reasoner integration.
"""

from __future__ import annotations

from rdflib import Graph

import owlrl

from synrax.schema.loader import load_schema


def reason(graph: Graph) -> Graph:
    """Apply OWL-RL reasoning to an RDF graph.

    Merges the ArchGraph OWL schema, then computes the entailment closure:
    - Transitive closure of :dependsOn and :callsTransitive
    - Inverse property inference (:usedBy from :dependsOn)
    - Subproperty propagation (:cascades → :usedBy)
    - Subclass hierarchy propagation

    Args:
        graph: Input RDF graph with extracted triples.

    Returns:
        The same graph, expanded with inferred triples.
    """
    schema = load_schema()
    for triple in schema:
        graph.add(triple)

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)
    return graph
