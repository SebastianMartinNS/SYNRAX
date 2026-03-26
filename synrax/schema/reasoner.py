"""synrax/schema/reasoner.py — OWL-RL reasoning over ArchGraph triples.

exports: reason(graph, schema_extensions) -> Graph
used_by: synrax/cli/main.py → export command | synrax/schema/__init__.py
rules:   Uses owlrl for OWL-RL entailment (transitive closure,
         inverse properties, subclass propagation).
         Merges schema.owl axioms into the graph before reasoning.
         Accepts optional extension schemas for project-specific ontologies.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial reasoner integration.
         claude-opus-4 | anthropic | 2026-03-22 | Dynamic schema extension support.
"""

from __future__ import annotations

from pathlib import Path

import owlrl
from rdflib import Graph

from synrax.schema.loader import load_schema


def reason(
    graph: Graph,
    schema_extensions: list[Path] | None = None,
    skip_schema: bool = False,
) -> Graph:
    """Apply OWL-RL reasoning to an RDF graph.

    Merges the ArchGraph OWL schema (plus any extensions), then computes
    the entailment closure:
    - Transitive closure of :dependsOn and :callsTransitive
    - Inverse property inference (:usedBy from :dependsOn)
    - Subproperty propagation (:cascades → :usedBy)
    - Subclass hierarchy propagation

    Args:
        graph: Input RDF graph with extracted triples.
        schema_extensions: Additional OWL/TTL files to merge before reasoning.
        skip_schema: If True, skip loading/merging the schema (caller already loaded it).

    Returns:
        The same graph, expanded with inferred triples.
    """
    if not skip_schema:
        schema = load_schema(extra=schema_extensions)
        for triple in schema:
            graph.add(triple)

    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)
    return graph
