"""synrax/extract/import_analyzer.py — AST-based import analysis for ground-truth dependencies.

exports: analyze_imports(path, root) -> list[dict] | resolve_import_to_file(import_path, root) -> Path | None | build_import_graph(root) -> Graph
used_by: synrax/extract/module_parser.py → parse_module | synrax/runtime/session_graph.py → ingest_file
rules:   Only creates edges for intra-project imports (excludes stdlib + third-party).
         Uses ast.parse, never regex on import lines.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, RDF, bind_namespaces

# stdlib top-level module names (frozen for Python 3.11+)
_STDLIB_TOP = frozenset(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else frozenset()


def _make_module_uri(module_path: str) -> str:
    """Create a URI-safe identifier from a module file path."""
    return module_path.replace("/", "_").replace("\\", "_").replace(".py", "").replace("-", "_")


def resolve_import_to_file(import_path: str, root: Path, source_file: Path | None = None) -> Path | None:
    """Map a dotted import path to a .py file within the project.

    Args:
        import_path: Dotted module path (e.g. 'django.db.models.indexes').
        root: Project root directory.
        source_file: Source file for resolving relative imports (leading dots stripped before call).

    Returns:
        Resolved Path if the import is intra-project, None otherwise.
    """
    parts = import_path.split(".")

    # Check if top-level is stdlib
    if parts[0] in _STDLIB_TOP:
        return None

    # Try as package (dir/__init__.py) then as module (.py)
    relative = Path(*parts)
    candidates = [
        root / relative / "__init__.py",
        root / relative.with_suffix(".py"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def analyze_imports(path: Path, root: Path) -> list[dict[str, str]]:
    """Extract all import statements from a Python file and resolve to intra-project files.

    Args:
        path: Path to the .py source file.
        root: Codebase root directory.

    Returns:
        List of dicts with keys: 'module' (relative path), 'imported_name', 'type' ('import'|'from').
    """
    root = root.resolve()
    path = path.resolve()

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    results: list[dict[str, str]] = []
    seen: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                resolved = resolve_import_to_file(alias.name, root)
                if resolved and resolved != path:
                    rel = str(resolved.relative_to(root)).replace("\\", "/")
                    if rel not in seen:
                        seen.add(rel)
                        results.append({
                            "module": rel,
                            "imported_name": alias.asname or alias.name.split(".")[-1],
                            "type": "import",
                        })

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue

            # Handle relative imports
            if node.level > 0:
                source_dir = path.parent
                # Walk up `level - 1` directories
                base_dir = source_dir
                for _ in range(node.level - 1):
                    base_dir = base_dir.parent
                module_path = node.module.replace(".", "/")
                abs_path_pkg = base_dir / module_path / "__init__.py"
                abs_path_mod = base_dir / f"{module_path}.py"

                resolved = None
                if abs_path_pkg.is_file():
                    resolved = abs_path_pkg.resolve()
                elif abs_path_mod.is_file():
                    resolved = abs_path_mod.resolve()
            else:
                resolved = resolve_import_to_file(node.module, root)

            if resolved and resolved != path:
                try:
                    rel = str(resolved.relative_to(root)).replace("\\", "/")
                except ValueError:
                    continue
                if rel not in seen:
                    seen.add(rel)
                    names = ", ".join(a.name for a in (node.names or []))
                    results.append({
                        "module": rel,
                        "imported_name": names or node.module.split(".")[-1],
                        "type": "from",
                    })

    return results


def build_import_graph(root: Path) -> Graph:
    """Walk all .py files under root and build arch:dependsOn triples from import analysis.

    Args:
        root: Project root directory.

    Returns:
        RDF graph with dependsOn triples for all intra-project imports.
    """
    root = root.resolve()
    g = Graph()
    bind_namespaces(g)

    for py_file in root.rglob("*.py"):
        # Skip hidden dirs, __pycache__
        if any(part.startswith((".", "__")) for part in py_file.relative_to(root).parts[:-1]):
            continue

        source_rel = str(py_file.relative_to(root)).replace("\\", "/")
        imports = analyze_imports(py_file, root)

        if not imports:
            continue

        source_uri = ARCH[_make_module_uri(source_rel)]
        g.add((source_uri, RDF.type, ARCH.Module))
        g.add((source_uri, ARCH.moduleName, Literal(source_rel, datatype=XSD.string)))

        for imp in imports:
            target_uri = ARCH[_make_module_uri(imp["module"])]
            g.add((source_uri, ARCH.dependsOn, target_uri))

    return g


def get_importers(target_path: str, root: Path) -> list[str]:
    """Find all files in the project that import a given file.

    Args:
        target_path: Relative path of the target file (e.g. 'db/connection.py').
        root: Project root directory.

    Returns:
        List of relative paths of files that import the target.
    """
    root = root.resolve()
    target_resolved = (root / target_path).resolve()
    importers: list[str] = []

    for py_file in root.rglob("*.py"):
        if any(part.startswith((".", "__")) for part in py_file.relative_to(root).parts[:-1]):
            continue
        if py_file.resolve() == target_resolved:
            continue

        imports = analyze_imports(py_file, root)
        for imp in imports:
            imp_resolved = (root / imp["module"]).resolve()
            if imp_resolved == target_resolved:
                rel = str(py_file.relative_to(root)).replace("\\", "/")
                importers.append(rel)
                break

    return importers
