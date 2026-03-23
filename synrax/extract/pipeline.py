"""synrax/extract/pipeline.py — Full codebase extraction pipeline.

exports: extract_codebase(root) -> Graph
used_by: synrax/cli/main.py → export command
rules:   Walks root for .codedna manifest + .py files with CodeDNA docstrings.
         Merges all per-file graphs into one unified graph.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial pipeline.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from synrax.extract.manifest import parse_manifest
from synrax.extract.module_parser import parse_module
from synrax.namespaces import bind_namespaces


def extract_codebase(root: Path) -> Graph:
    """Extract all CodeDNA annotations from a codebase into a single RDF graph.

    Args:
        root: Root directory of the codebase.

    Returns:
        Merged RDF graph with all extracted triples.
    """
    root = Path(root).resolve()
    g = Graph()
    bind_namespaces(g)

    # Parse .codedna manifest
    manifest_path = root / ".codedna"
    if manifest_path.is_file():
        manifest_graph = parse_manifest(manifest_path)
        for triple in manifest_graph:
            g.add(triple)

    # Walk Python files for CodeDNA docstrings
    for py_file in root.rglob("*.py"):
        # Skip hidden dirs, __pycache__, etc.
        if any(part.startswith((".", "__")) for part in py_file.relative_to(root).parts[:-1]):
            continue

        try:
            module_graph = parse_module(py_file, project="", root=root)
            for triple in module_graph:
                g.add(triple)
        except Exception:
            # Skip files that fail to parse (syntax errors, encoding, etc.)
            continue

    return g
