"""synrax/schema/loader.py — Load OWL schema and SHACL shapes with dynamic extension support.

exports: load_schema(extra) -> Graph
         | load_shapes(extra) -> Graph
         | discover_extensions(root) -> list[Path]
used_by: synrax/schema/__init__.py | synrax/schema/reasoner.py | synrax/schema/validator.py
rules:   Base schema/shapes are always loaded from bundled files.
         Extra OWL/TTL files can be merged in for project-specific extensions.
         .codedna manifest 'extensions' field drives auto-discovery.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial loader.
         claude-opus-4 | anthropic | 2026-03-22 | Dynamic schema/shapes with extension support.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from rdflib import Graph

from synrax.namespaces import bind_namespaces

_SCHEMA_DIR = Path(__file__).parent


def load_schema(extra: list[Path] | None = None) -> Graph:
    """Load the ArchGraph OWL ontology, optionally merging extension schemas.

    Args:
        extra: Additional OWL/TTL files to merge into the base schema.

    Returns:
        Graph containing the merged ontology.
    """
    g = Graph()
    bind_namespaces(g)
    g.parse(str(_SCHEMA_DIR / "schema.owl"), format="turtle")

    for ext_path in extra or []:
        if ext_path.is_file():
            fmt = "turtle" if ext_path.suffix in (".ttl", ".owl") else "xml"
            g.parse(str(ext_path), format=fmt)

    return g


def load_shapes(extra: list[Path] | None = None) -> Graph:
    """Load the ArchGraph SHACL shapes, optionally merging extension shapes.

    Args:
        extra: Additional SHACL TTL files to merge into the base shapes.

    Returns:
        Graph containing the merged shapes.
    """
    g = Graph()
    bind_namespaces(g)
    g.parse(str(_SCHEMA_DIR / "shapes.ttl"), format="turtle")

    for ext_path in extra or []:
        if ext_path.is_file():
            fmt = "turtle" if ext_path.suffix in (".ttl", ".owl") else "xml"
            g.parse(str(ext_path), format=fmt)

    return g


def discover_extensions(root: Path) -> tuple[list[Path], list[Path]]:
    """Discover schema and shape extensions from a project's .codedna manifest.

    Looks for an 'extensions' field in the .codedna YAML manifest.
    Extension files are resolved relative to the project root.

    Example .codedna:
        project: my-iot-device
        extensions:
          schema: [schema_hw.owl, schema_radio.owl]
          shapes: [shapes_hw.ttl]

    Args:
        root: Project root directory containing .codedna.

    Returns:
        Tuple of (schema_extensions, shapes_extensions) as resolved Paths.
    """
    manifest = root / ".codedna"
    if not manifest.is_file():
        return [], []

    try:
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except Exception:
        return [], []

    if not isinstance(data, dict):
        return [], []

    extensions = data.get("extensions")
    if not isinstance(extensions, dict):
        return [], []

    schema_files: list[Path] = []
    shapes_files: list[Path] = []

    for rel in extensions.get("schema", []):
        p = (root / rel).resolve()
        if p.is_file():
            schema_files.append(p)

    for rel in extensions.get("shapes", []):
        p = (root / rel).resolve()
        if p.is_file():
            shapes_files.append(p)

    return schema_files, shapes_files
