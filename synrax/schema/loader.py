"""synrax/schema/loader.py — Load OWL schema and SHACL shapes from bundled .ttl/.owl files.

exports: load_schema() -> Graph | load_shapes() -> Graph
used_by: synrax/schema/__init__.py | synrax/schema/reasoner.py | synrax/schema/validator.py
rules:   Always loads from the bundled files in this package directory.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial loader.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from synrax.namespaces import bind_namespaces

_SCHEMA_DIR = Path(__file__).parent


def load_schema() -> Graph:
    """Load the ArchGraph OWL ontology."""
    g = Graph()
    bind_namespaces(g)
    g.parse(str(_SCHEMA_DIR / "schema.owl"), format="turtle")
    return g


def load_shapes() -> Graph:
    """Load the ArchGraph SHACL shapes."""
    g = Graph()
    bind_namespaces(g)
    g.parse(str(_SCHEMA_DIR / "shapes.ttl"), format="turtle")
    return g
