"""synrax/query/engine.py — SPARQL query execution against RDF graphs.

exports: run_query(name, turtle_file, **params) -> list[dict]
used_by: synrax/cli/main.py → query command | synrax/query/__init__.py
rules:   Loads template, substitutes params, executes on rdflib Graph.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial query engine.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from synrax.namespaces import bind_namespaces
from synrax.query.templates_loader import load_template


def run_query(name: str, turtle_file: Path, **params: str) -> list[dict]:
    """Execute a named SPARQL query template against an RDF/Turtle file.

    Args:
        name: Template name (matches a .rq file in templates/).
        turtle_file: Path to the Turtle file to query.
        **params: Substitution parameters for the template (e.g., module="billing_invoice_service").

    Returns:
        List of result dicts, one per row.
    """
    query_str = load_template(name)

    # Simple parameter substitution: {{param_name}} → value
    for key, value in params.items():
        query_str = query_str.replace(f"{{{{{key}}}}}", value)

    g = Graph()
    bind_namespaces(g)
    g.parse(str(turtle_file), format="turtle")

    results = []
    for row in g.query(query_str):
        results.append({str(var): str(val) for var, val in zip(row.labels, row)})

    return results
