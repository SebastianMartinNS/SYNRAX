"""synrax/extract/manifest.py — .codedna YAML manifest parser → RDF triples.

exports: parse_manifest(path) -> Graph
used_by: synrax/extract/pipeline.py → extract_codebase
rules:   Manifest MUST have 'project' and 'packages' keys.
         Each package generates an arch:Package triple with packageName and purpose.
         depends_on generates arch:dependsOn triples between packages.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial manifest parser.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, RDF, bind_namespaces


def _make_package_uri(project: str, package_path: str) -> str:
    """Create a URI-safe identifier for a package."""
    clean = package_path.rstrip("/").replace("/", "_").replace("-", "_")
    return f"{project}_{clean}"


def parse_manifest(path: Path) -> Graph:
    """Parse a .codedna YAML manifest and return an RDF graph.

    Args:
        path: Path to the .codedna file.

    Returns:
        Graph containing arch:Package triples.

    Raises:
        ValueError: If the manifest is missing required fields.
    """
    g = Graph()
    bind_namespaces(g)

    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid .codedna manifest: expected mapping, got {type(data).__name__}")

    project = data.get("project")
    if not project:
        raise ValueError("Missing required field 'project' in .codedna manifest")

    packages = data.get("packages", {})
    if not isinstance(packages, dict):
        raise ValueError("'packages' must be a mapping in .codedna manifest")

    for pkg_path, pkg_info in packages.items():
        if pkg_info is None:
            pkg_info = {}

        pkg_uri = ARCH[_make_package_uri(project, pkg_path)]

        g.add((pkg_uri, RDF.type, ARCH.Package))
        g.add((pkg_uri, ARCH.packageName, Literal(pkg_path, datatype=XSD.string)))

        purpose = pkg_info.get("purpose", "")
        if purpose:
            g.add((pkg_uri, ARCH.purpose, Literal(purpose, datatype=XSD.string)))

        depends_on = pkg_info.get("depends_on", [])
        if isinstance(depends_on, list):
            for dep_path in depends_on:
                dep_uri = ARCH[_make_package_uri(project, dep_path)]
                g.add((pkg_uri, ARCH.dependsOn, dep_uri))

    return g
