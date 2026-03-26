"""synrax/runtime/session_graph.py — Incremental in-memory knowledge graph with lazy reasoning.

exports: SessionGraph
used_by: synrax/runtime/tools.py → make_synrax_tools | synrax/cli/main.py → serve
rules:   Reasoning is lazy — only runs when a query is executed and the graph is dirty.
         Thread-safe for single-writer/multi-reader via the dirty flag pattern.
"""

from __future__ import annotations

import copy
import statistics
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.extract.import_analyzer import analyze_imports
from synrax.extract.module_parser import parse_module
from synrax.namespaces import ARCH, RDF, bind_namespaces, make_module_uri, uri_to_path
from synrax.schema.loader import load_schema
from synrax.schema.reasoner import reason
from synrax.query.templates_loader import load_template


# Keep backward-compatible alias
_make_module_uri = make_module_uri


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

        # EXP-5: Track edge sources for confidence labels
        self._edge_sources: dict[tuple[str, str], str] = {}

        # EXP-2: Track files visited (read) by the agent
        self._visited_files: set[str] = set()

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

        # Snapshot edges before CodeDNA parsing to detect annotated edges
        edges_before = set(self._raw_graph.triples((None, ARCH.dependsOn, None)))

        # Layer 1: Parse CodeDNA annotations (exports, used_by, rules, agent)
        try:
            module_graph = parse_module(abs_path, project="", root=self._root)
            for triple in module_graph:
                self._raw_graph.add(triple)
        except Exception:
            pass

        # Track annotated edges from parse_module
        edges_after_codedna = set(self._raw_graph.triples((None, ARCH.dependsOn, None)))
        codedna_edges = edges_after_codedna - edges_before
        uri_frag = _make_module_uri(rel_path)
        for s, _p, o in codedna_edges:
            s_name = str(s).replace("http://archgraph.example.org/", "")
            o_name = str(o).replace("http://archgraph.example.org/", "")
            if s_name == uri_frag:
                self._edge_sources[(rel_path, self._uri_to_path(o_name))] = "structural"
            else:
                self._edge_sources[(self._uri_to_path(s_name), rel_path)] = "annotated"

        # Layer 2: AST import analysis (always runs, even without CodeDNA annotations)
        # This is Synrax's structural analysis — independent of CodeDNA.
        try:
            import_results = analyze_imports(abs_path, self._root)
            module_uri = ARCH[uri_frag]
            for imp in import_results:
                imp_uri = ARCH[_make_module_uri(imp["module"])]
                # Skip if already added by parse_module (Graph has set semantics, but track source)
                if (module_uri, ARCH.dependsOn, imp_uri) not in self._raw_graph:
                    self._raw_graph.add((module_uri, ARCH.dependsOn, imp_uri))
                # Always mark as structural (AST ground truth)
                imp_path = imp["module"]
                if (rel_path, imp_path) not in self._edge_sources:
                    self._edge_sources[(rel_path, imp_path)] = "structural"
        except Exception:
            pass

        # Ensure the module node exists even without annotations
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
        reason(self._reasoned_graph, skip_schema=True)
        self._dirty = False

        # EXP-5: Track inferred edges (new dependsOn triples from reasoning)
        raw_deps = set(self._raw_graph.triples((None, ARCH.dependsOn, None)))
        reasoned_deps = set(self._reasoned_graph.triples((None, ARCH.dependsOn, None)))
        for s, _p, o in reasoned_deps - raw_deps:
            s_name = str(s).replace("http://archgraph.example.org/", "")
            o_name = str(o).replace("http://archgraph.example.org/", "")
            key = (self._uri_to_path(s_name), self._uri_to_path(o_name))
            if key not in self._edge_sources:
                self._edge_sources[key] = "inferred"

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

    # ── EXP-5: URI ↔ path helpers ──────────────────────────────────────

    def get_edge_source(self, from_path: str, to_path: str) -> str:
        """Return the provenance of a dependency edge.

        Args:
            from_path: Source module path (e.g. 'models/order.py').
            to_path: Target module path (e.g. 'db/connection.py').

        Returns:
            One of 'structural', 'annotated', 'inferred', or 'unknown'.
        """
        return self._edge_sources.get((from_path, to_path), "unknown")

    @staticmethod
    def _uri_to_path(uri_fragment: str) -> str:
        """Convert URI fragment back to approximate file path.

        Delegates to the centralized uri_to_path in namespaces.py.
        """
        return uri_to_path(uri_fragment)

    # ── EXP-2: Visited file tracking ───────────────────────────────────

    def mark_visited(self, path: str) -> None:
        """Record that the agent read this file (for boundary analysis)."""
        if isinstance(path, str):
            abs_path = (self._root / path).resolve()
        else:
            abs_path = path.resolve()
        try:
            rel = str(abs_path.relative_to(self._root)).replace("\\", "/")
        except ValueError:
            rel = str(path)
        self._visited_files.add(rel)

    def get_boundary_status(self) -> dict:
        """Compute how much of the impact zone the agent has explored.

        Returns dict with:
          explored_pct: int (0-100)
          remaining_in_scope: list[str] — files in impact zone not yet visited
          out_of_scope_sample: list[str] — files with no connection to visited set
        """
        if not self._visited_files:
            return {}

        # Get all modules in the impact zone of visited files
        in_scope: set[str] = set()
        for vf in self._visited_files:
            uri = _make_module_uri(vf)
            try:
                # Files that depend on this file
                impact = self.query_template("impact_analysis", module=uri)
                for r in impact:
                    in_scope.add(r.get("name", ""))
                # Files this file depends on
                deps = self.query_template("deps_of", module=uri)
                for r in deps:
                    in_scope.add(r.get("name", ""))
            except Exception:
                pass
        in_scope |= self._visited_files
        in_scope.discard("")

        # All ingested files
        all_files = set(self._ingested_files)

        # Exclude __init__.py from scope counting — they are routing hubs,
        # not real targets.  Keep them in remaining list for completeness
        # but don't let them inflate the denominator / deflate explored_pct.
        _is_init = lambda p: p.endswith("__init__.py")
        meaningful_scope = {p for p in in_scope if not _is_init(p)}
        meaningful_visited = {p for p in self._visited_files if not _is_init(p)}

        remaining = sorted(in_scope - self._visited_files)
        remaining_meaningful = [p for p in remaining if not _is_init(p)]
        out_of_scope = sorted(all_files - in_scope)
        explored = len(meaningful_visited & meaningful_scope)
        total_scope = len(meaningful_scope) or 1

        return {
            "explored_pct": round(100 * explored / total_scope),
            "remaining_in_scope": remaining_meaningful,
            "out_of_scope_sample": out_of_scope[:10],
        }

    # ── Tension engine ────────────────────────────────────────────────

    def compute_tension(self) -> dict:
        """Compute tension between explored and unexplored impact zone.

        Returns dict with:
          blast_zone_total: int — meaningful files in impact zone
          blast_zone_unvisited: int — unvisited meaningful files in impact zone
          tension_ratio: float (0.0=fully explored, 1.0=nothing explored)
          high_tension_files: list[str] — top 3 unvisited files ranked by in-degree
          explored_pct: int (0-100)
        """
        if not self._visited_files:
            # Pre-ingested but nothing visited — maximum tension
            meaningful = {f for f in self._ingested_files
                         if not f.endswith("__init__.py")}
            return {
                "blast_zone_total": len(meaningful),
                "blast_zone_unvisited": len(meaningful),
                "tension_ratio": 1.0 if meaningful else 0.0,
                "high_tension_files": [],
                "explored_pct": 0,
            }

        boundary = self.get_boundary_status()
        if not boundary:
            return {
                "blast_zone_total": 0,
                "blast_zone_unvisited": 0,
                "tension_ratio": 0.0,
                "high_tension_files": [],
                "explored_pct": 0,
            }

        remaining = boundary.get("remaining_in_scope", [])
        explored_pct = boundary.get("explored_pct", 0)

        # Build in_scope the same way as get_boundary_status
        _is_init = lambda p: p.endswith("__init__.py")
        in_scope: set[str] = set()
        for vf in self._visited_files:
            uri = _make_module_uri(vf)
            try:
                impact = self.query_template("impact_analysis", module=uri)
                for r in impact:
                    in_scope.add(r.get("name", ""))
                deps = self.query_template("deps_of", module=uri)
                for r in deps:
                    in_scope.add(r.get("name", ""))
            except Exception:
                pass
        in_scope |= self._visited_files
        in_scope.discard("")
        meaningful_scope = {p for p in in_scope if not _is_init(p)}
        meaningful_remaining = [p for p in remaining if not _is_init(p)]
        total = len(meaningful_scope) or 1
        unvisited = len(meaningful_remaining)

        # Rank unvisited by in-degree (most dependents first)
        degrees: dict[str, int] = {}
        try:
            rows = self.query_template("node_roles")
            for r in rows:
                name = r.get("name", "")
                if name:
                    degrees[name] = int(r.get("in_deg", "0"))
        except Exception:
            pass

        high_tension = sorted(
            meaningful_remaining,
            key=lambda f: -degrees.get(f, 0),
        )[:3]

        return {
            "blast_zone_total": total,
            "blast_zone_unvisited": unvisited,
            "tension_ratio": round(unvisited / total, 2) if total else 0.0,
            "high_tension_files": high_tension,
            "explored_pct": explored_pct,
        }

    # ── EXP-3: Node role classification ────────────────────────────────

    def classify_node_roles(self) -> dict[str, str]:
        """Classify each ingested module as 'hub', 'leaf', or 'connector'.

        hub: __init__.py OR in-degree > 2× median
        leaf: in-degree ≤ median and not hub
        connector: everything else

        Uses the node_roles.rq template which counts only direct (non-transitive)
        dependencies to avoid inflated degrees on reasoned graphs.

        Returns dict mapping module path → role.
        """
        try:
            rows = self.query_template("node_roles")
        except Exception:
            return {}

        degrees: dict[str, int] = {}
        for r in rows:
            name = r.get("name", "")
            if name:
                degrees[name] = int(r.get("in_deg", "0"))

        if not degrees:
            return {}

        # Include modules with zero in-degree
        for f in self._ingested_files:
            if f not in degrees:
                degrees[f] = 0

        values = list(degrees.values())
        median_deg = statistics.median(values) if values else 0
        threshold = max(2 * median_deg, 2)  # at least 2

        roles: dict[str, str] = {}
        for name, deg in degrees.items():
            if name.endswith("__init__.py") or deg > threshold:
                roles[name] = "hub"
            elif deg <= median_deg:
                roles[name] = "leaf"
            else:
                roles[name] = "connector"

        return roles

    # ── EXP-5: Architectural level inference ───────────────────────────

    @staticmethod
    def infer_architectural_level(module_path: str) -> str:
        """Infer the architectural level of a module from its file path.

        Heuristic classification:
          - '__init__.py' → 'routing'
          - 'base/' in path → 'base-layer'
          - backend dirs (mysql/, postgresql/, oracle/, sqlite3/) → 'backend-impl'
          - 'tests/' or 'test_' → 'test'
          - everything else → 'feature'
        """
        parts = module_path.lower().replace("\\", "/").split("/")
        filename = parts[-1] if parts else ""

        if filename == "__init__.py":
            return "routing"
        if "base" in parts:
            return "base-layer"
        _BACKEND_DIRS = {"mysql", "postgresql", "oracle", "sqlite3", "sqlite"}
        if any(p in _BACKEND_DIRS for p in parts):
            return "backend-impl"
        if "tests" in parts or filename.startswith("test_"):
            return "test"
        return "feature"

    # ── Edge provenance serialization ──────────────────────────────────

    def serialize_provenance(self) -> dict[str, list[dict[str, str]]]:
        """Serialize edge provenance data for persistence.

        Returns dict with keys: 'edges' (list of {from, to, source}).
        """
        edges = []
        for (from_path, to_path), source in sorted(self._edge_sources.items()):
            edges.append({"from": from_path, "to": to_path, "source": source})
        return {"edges": edges}

    def load_provenance(self, data: dict[str, list[dict[str, str]]]) -> None:
        """Load edge provenance data from a serialized dict."""
        for edge in data.get("edges", []):
            key = (edge["from"], edge["to"])
            self._edge_sources[key] = edge["source"]
