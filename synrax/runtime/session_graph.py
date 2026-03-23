"""synrax/runtime/session_graph.py — Incremental in-memory knowledge graph with lazy reasoning.

exports: SessionGraph
used_by: synrax/runtime/tools.py → make_synrax_tools | synrax/cli/main.py → serve
rules:   Reasoning is lazy — only runs when a query is executed and the graph is dirty.
         Thread-safe for single-writer/multi-reader via the dirty flag pattern.
"""

from __future__ import annotations

import copy
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.extract.import_analyzer import analyze_imports
from synrax.extract.module_parser import parse_module
from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.schema.loader import load_schema
from synrax.schema.reasoner import reason
from synrax.query.templates_loader import load_template


def _make_module_uri(module_path: str) -> str:
    return module_path.replace("/", "_").replace("\\", "_").replace(".py", "").replace("-", "_")


class SessionGraph:
    """Incremental knowledge graph that grows as the agent reads files.

    On ingest: parses CodeDNA annotations + AST imports, adds raw triples.
    On query: applies OWL-RL reasoning lazily (only if graph changed).
    """

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._raw_graph = Graph()
        bind_namespaces(self._raw_graph)

        # Pre-load OWL schema axioms into raw graph
        schema = load_schema()
        for triple in schema:
            self._raw_graph.add(triple)

        self._reasoned_graph: Graph | None = None
        self._dirty = True  # schema loaded → needs initial reasoning
        self._ingested_files: set[str] = set()
        self._raw_count_before_schema = 0
        self._schema_triple_count = len(self._raw_graph)

    @property
    def file_count(self) -> int:
        """Number of files ingested so far."""
        return len(self._ingested_files)

    @property
    def raw_triple_count(self) -> int:
        """Number of raw triples (excluding schema)."""
        return len(self._raw_graph) - self._schema_triple_count

    @property
    def reasoned_triple_count(self) -> int:
        """Number of triples after reasoning (excluding schema). Returns 0 if not yet reasoned."""
        if self._reasoned_graph is None:
            return 0
        return len(self._reasoned_graph) - self._schema_triple_count

    def ingest_file(self, path: str | Path) -> int:
        """Parse a file's annotations + imports and add triples to the graph.

        Args:
            path: Relative or absolute path to a .py file.

        Returns:
            Number of new triples added (0 if file was already ingested or has no annotations).
        """
        if isinstance(path, str):
            # Normalize: accept both relative and absolute paths
            abs_path = (self._root / path).resolve()
        else:
            abs_path = path.resolve()

        if not abs_path.is_file() or abs_path.suffix != ".py":
            return 0

        try:
            rel_path = str(abs_path.relative_to(self._root)).replace("\\", "/")
        except ValueError:
            return 0

        if rel_path in self._ingested_files:
            return 0

        before = len(self._raw_graph)

        # Parse CodeDNA annotations
        try:
            module_graph = parse_module(abs_path, project="", root=self._root)
            for triple in module_graph:
                self._raw_graph.add(triple)
        except Exception:
            pass

        # Ensure the module node exists even without annotations (for import edges)
        module_uri = ARCH[_make_module_uri(rel_path)]
        if (module_uri, RDF.type, ARCH.Module) not in self._raw_graph:
            self._raw_graph.add((module_uri, RDF.type, ARCH.Module))
            self._raw_graph.add((module_uri, ARCH.moduleName, Literal(rel_path, datatype=XSD.string)))

        after = len(self._raw_graph)
        added = after - before

        self._ingested_files.add(rel_path)

        if added > 0:
            self._dirty = True

        return added

    def ensure_reasoned(self) -> Graph:
        """Return the reasoned graph, applying OWL-RL if dirty.

        Returns:
            The fully-reasoned graph.
        """
        if not self._dirty and self._reasoned_graph is not None:
            return self._reasoned_graph

        # Deep copy raw graph, then reason over the copy
        self._reasoned_graph = copy.deepcopy(self._raw_graph)
        reason(self._reasoned_graph)
        self._dirty = False
        return self._reasoned_graph

    def query(self, sparql: str, **params: str) -> list[dict[str, str]]:
        """Execute a SPARQL query against the reasoned graph.

        Args:
            sparql: SPARQL query string (may contain {{param}} placeholders).
            **params: Substitution parameters.

        Returns:
            List of result dicts, one per row.
        """
        g = self.ensure_reasoned()

        for key, value in params.items():
            sparql = sparql.replace(f"{{{{{key}}}}}", value)

        results = []
        for row in g.query(sparql):
            results.append({str(var): str(val) for var, val in zip(row.labels, row)})
        return results

    def query_template(self, name: str, **params: str) -> list[dict[str, str]]:
        """Execute a named SPARQL template against the reasoned graph.

        Args:
            name: Template name (without .rq extension).
            **params: Substitution parameters.

        Returns:
            List of result dicts, one per row.
        """
        template = load_template(name)
        return self.query(template, **params)

    def ingest_all(self) -> int:
        """Pre-ingest all .py files under root. Returns total triples added."""
        total = 0
        for py_file in self._root.rglob("*.py"):
            if any(part.startswith((".", "__")) for part in py_file.relative_to(self._root).parts[:-1]):
                continue
            total += self.ingest_file(py_file)
        return total
