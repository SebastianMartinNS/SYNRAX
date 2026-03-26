"""benchmark_agent.py — SWE-bench style agentic benchmark on real public codebases.

The LLM navigates the codebase via tool calls (read_file, grep, list_dir, etc.).
In Synrax mode it also gets graph query tools (blast_radius, dependencies, cycles).
We measure: F1, Precision, Recall, Pass@1, tool calls, files read, tokens.

Repos: click (8.1.7), rich (v13.7.1), httpx (0.27.0) — pinned tags, reproducible.
Ground truth: computed from AST dependency graph, not hand-written keywords.

Usage:
    py benchmark_agent.py --dry-run                          # Show tasks + ground truth, no API
    py benchmark_agent.py --repo click                       # Single repo, default model
    py benchmark_agent.py --all-repos --all-models           # Full benchmark
    py benchmark_agent.py --repo click --model deepseek/deepseek-chat-v3-0324
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
import time
import zipfile
from collections import defaultdict, deque
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "google/gemini-2.5-flash",
    "anthropic/claude-sonnet-4",
    "deepseek/deepseek-chat-v3-0324",
    "openai/gpt-4.1-mini",
]

REPOS: dict[str, dict[str, str]] = {
    "click": {
        "url": "https://github.com/pallets/click/archive/refs/tags/8.1.7.zip",
        "project_root": "src",
        "package_dir": "src/click",
        "package_name": "click",
        "description": "CLI toolkit by Pallets (~15 modules)",
    },
    "rich": {
        "url": "https://github.com/Textualize/rich/archive/refs/tags/v13.7.1.zip",
        "project_root": ".",
        "package_dir": "rich",
        "package_name": "rich",
        "description": "Terminal rich-text library (~77 modules)",
    },
    "httpx": {
        "url": "https://github.com/encode/httpx/archive/refs/tags/0.27.0.zip",
        "project_root": ".",
        "package_dir": "httpx",
        "package_name": "httpx",
        "description": "Async HTTP client (~22 modules)",
    },
}

CACHE_DIR = Path(__file__).parent / ".bench_cache"
MAX_TURNS = 25          # max tool-call rounds per question
MAX_FILE_CHARS = 8_000  # cap per read_file to avoid blowing context
PASS_THRESHOLD = 0.5    # F1 >= this counts as pass@1
TENSION_ALERT_INTERVAL = 3  # inject tension alert every N file-reads


# ---------------------------------------------------------------------------
# REPO DOWNLOAD (reused from benchmark_real.py)
# ---------------------------------------------------------------------------

def download_repo(name: str, config: dict[str, str]) -> tuple[Path, Path]:
    CACHE_DIR.mkdir(exist_ok=True)
    extract_base = CACHE_DIR / name

    if extract_base.exists():
        top = _find_top(extract_base)
        proj = top / config["project_root"]
        pkg = top / config["package_dir"]
        if pkg.is_dir():
            return proj.resolve(), pkg.resolve()

    url = config["url"]
    print(f"  Downloading {name} ...", end=" ", flush=True)
    req = Request(url, headers={"User-Agent": "synrax-benchmark/1.0"})
    buf = BytesIO()
    with urlopen(req, timeout=120) as resp:
        buf.write(resp.read())
    buf.seek(0)
    print("extracting ...", end=" ", flush=True)

    extract_base.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(buf) as zf:
        zf.extractall(extract_base)
    print("done.")

    top = _find_top(extract_base)
    return (top / config["project_root"]).resolve(), (top / config["package_dir"]).resolve()


def _find_top(base: Path) -> Path:
    children = [c for c in base.iterdir() if c.is_dir() and not c.name.startswith(".")]
    return children[0] if len(children) == 1 else base


# ---------------------------------------------------------------------------
# DEPENDENCY GRAPH (pure AST — honest ground truth)
# ---------------------------------------------------------------------------

def build_dep_graph(project_root: Path, package_dir: Path) -> dict[str, set[str]]:
    project_root = project_root.resolve()
    graph: dict[str, set[str]] = {}

    for py_file in sorted(package_dir.rglob("*.py")):
        try:
            rel_parts = py_file.relative_to(package_dir).parts
        except ValueError:
            continue
        if any(p.startswith((".", "__pycache__")) for p in rel_parts[:-1]):
            continue

        src_rel = str(py_file.relative_to(project_root)).replace("\\", "/")
        graph.setdefault(src_rel, set())

        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(py_file))
        except (SyntaxError, UnicodeDecodeError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    resolved = _resolve_import(alias.name, project_root)
                    if resolved and resolved != py_file:
                        _add_edge(graph, src_rel, resolved, project_root)
            elif isinstance(node, ast.ImportFrom):
                if node.module is None and node.level > 0:
                    base = py_file.parent
                    for _ in range(node.level - 1):
                        base = base.parent
                    for alias in (node.names or []):
                        for cand in [base / alias.name / "__init__.py",
                                     base / f"{alias.name}.py"]:
                            if cand.is_file() and cand.resolve() != py_file:
                                _add_edge(graph, src_rel, cand.resolve(), project_root)
                                break
                    continue
                if node.module is None:
                    continue
                if node.level > 0:
                    base = py_file.parent
                    for _ in range(node.level - 1):
                        base = base.parent
                    mod_path = node.module.replace(".", "/")
                    resolved = None
                    for cand in [base / mod_path / "__init__.py", base / f"{mod_path}.py"]:
                        if cand.is_file():
                            resolved = cand.resolve()
                            break
                else:
                    resolved = _resolve_import(node.module, project_root)
                if resolved and resolved != py_file:
                    _add_edge(graph, src_rel, resolved, project_root)

    return graph


def _resolve_import(import_path: str, root: Path) -> Path | None:
    _STDLIB = frozenset(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else frozenset()
    parts = import_path.split(".")
    if parts[0] in _STDLIB:
        return None
    rel = Path(*parts)
    for cand in [root / rel / "__init__.py", root / rel.with_suffix(".py")]:
        if cand.is_file():
            return cand.resolve()
    return None


def _add_edge(graph: dict[str, set[str]], src: str, tgt: Path, root: Path) -> None:
    try:
        tgt_rel = str(tgt.relative_to(root)).replace("\\", "/")
        graph[src].add(tgt_rel)
        graph.setdefault(tgt_rel, set())
    except ValueError:
        pass


def _reverse_graph(graph: dict[str, set[str]]) -> dict[str, set[str]]:
    rev: dict[str, set[str]] = defaultdict(set)
    for node in graph:
        rev.setdefault(node, set())
    for src, targets in graph.items():
        for tgt in targets:
            rev[tgt].add(src)
    return dict(rev)


def _bfs(graph: dict[str, set[str]], start: str) -> set[str]:
    visited: set[str] = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, set()):
            if neighbor not in visited and neighbor != start:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def _shortest_path(graph: dict[str, set[str]], start: str, end: str) -> list[str] | None:
    if start == end:
        return [start]
    visited = {start}
    queue: deque[list[str]] = deque([[start]])
    while queue:
        path = queue.popleft()
        for neighbor in graph.get(path[-1], set()):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None


def _find_cycles(graph: dict[str, set[str]]) -> list[tuple[str, str]]:
    cycles = []
    seen: set[tuple[str, str]] = set()
    for src, targets in graph.items():
        for tgt in targets:
            if src in graph.get(tgt, set()):
                pair = tuple(sorted([src, tgt]))
                if pair not in seen:
                    seen.add(pair)
                    cycles.append((pair[0], pair[1]))
    return sorted(cycles)


# ---------------------------------------------------------------------------
# QUESTION GENERATION (same as benchmark_real.py, reused)
# ---------------------------------------------------------------------------

def generate_questions(
    graph: dict[str, set[str]],
    package_name: str,
) -> list[dict[str, Any]]:
    rev = _reverse_graph(graph)
    all_modules = sorted(graph.keys())
    real_modules = [m for m in all_modules if not m.endswith("__init__.py")]
    if not real_modules:
        real_modules = all_modules

    questions: list[dict[str, Any]] = []

    # Q1: Blast radius of highest-impact module
    impact = {m: len(_bfs(rev, m)) for m in real_modules}
    top_mod = max(real_modules, key=lambda m: impact[m])
    top_deps = sorted(_bfs(rev, top_mod))
    if top_deps:
        questions.append({
            "id": f"{package_name}_Q1_blast",
            "task": (
                f"Find all modules that would be affected if `{top_mod}` is completely rewritten. "
                f"List ALL modules that directly or indirectly depend on it. "
                f"Give your final answer as a list of file paths."
            ),
            "ground_truth": set(top_deps),
            "type": "blast_radius",
        })

    # Q2: All deps of the deepest module
    dep_depth = {m: len(_bfs(graph, m)) for m in real_modules}
    deep_mod = max(real_modules, key=lambda m: dep_depth[m])
    deep_deps = sorted(_bfs(graph, deep_mod))
    if deep_deps:
        questions.append({
            "id": f"{package_name}_Q2_deps",
            "task": (
                f"What are ALL the direct and indirect dependencies of `{deep_mod}`? "
                f"Trace the full dependency tree. List every module it depends on (transitively)."
            ),
            "ground_truth": set(deep_deps),
            "type": "dependency_trace",
        })

    # Q3: Path between distant modules
    best_path: list[str] | None = None
    best_src = best_tgt = ""
    for m in real_modules:
        trans = _bfs(graph, m)
        direct = graph.get(m, set())
        indirect = trans - direct
        for tgt in sorted(indirect):
            p = _shortest_path(graph, m, tgt)
            if p and (best_path is None or len(p) > len(best_path)):
                best_path, best_src, best_tgt = p, m, tgt

    if best_path and len(best_path) >= 3:
        questions.append({
            "id": f"{package_name}_Q3_path",
            "task": (
                f"Is there a dependency chain from `{best_src}` to `{best_tgt}`? "
                f"If yes, trace the exact sequence of imports that connects them."
            ),
            "ground_truth": set(best_path),
            "type": "path_trace",
        })

    # Q4: Leaf modules
    leaves = sorted(m for m in real_modules if not graph.get(m, set()))
    if leaves:
        questions.append({
            "id": f"{package_name}_Q4_leaves",
            "task": (
                f"Which modules in {package_name} have ZERO internal imports "
                f"(they don't import any other module from the project)? List all of them."
            ),
            "ground_truth": set(leaves),
            "type": "leaf_detection",
        })

    # Q5: Hub module
    in_deg: dict[str, int] = defaultdict(int)
    for targets in graph.values():
        for t in targets:
            in_deg[t] += 1
    if in_deg:
        hub = max(real_modules, key=lambda m: in_deg.get(m, 0))
        importers = sorted(rev.get(hub, set()))
        if importers:
            questions.append({
                "id": f"{package_name}_Q5_hub",
                "task": (
                    f"Which single module in {package_name} is imported by the most other modules? "
                    f"Name it and list ALL modules that directly import it."
                ),
                "ground_truth": set([hub] + importers),
                "type": "hub_identification",
            })

    # Q6: Circular deps
    cycles = _find_cycles(graph)
    if cycles:
        cycle_mods = sorted(set(m for pair in cycles for m in pair))
        questions.append({
            "id": f"{package_name}_Q6_circular",
            "task": (
                f"Find ALL circular (mutual) import dependencies in {package_name}. "
                f"List every pair of modules that import each other."
            ),
            "ground_truth": set(cycle_mods),
            "type": "cycle_detection",
        })

    return questions


# ---------------------------------------------------------------------------
# SANDBOX TOOLS — what the LLM agent can call
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DOUBLE HELIX — Synrax navigation injected into read_file results
# ---------------------------------------------------------------------------

def _edge_label(session: Any, source_path: str, target_path: str) -> str:
    """Return 'annotated' or 'structural' label for an edge, or '' if unknown."""
    if not hasattr(session, '_edge_sources'):
        return ""
    return session._edge_sources.get((source_path, target_path), "")


def _build_nav_hint(session: Any, path: str, package_name: str) -> str:
    """Build a [Synrax Navigation] block for a file from the live graph.

    Capped to 3 Used-by / 5 Depends-on, with edge provenance labels.
    Includes boundary check after 2+ files visited.
    """
    from synrax.namespaces import make_module_uri
    uri = make_module_uri(path)
    parts: list[str] = []

    ref_level = session.infer_architectural_level(path)

    def _sort_by_relevance(names: list[str], ref_path: str) -> list[str]:
        ref_pkg = "/".join(ref_path.split("/")[:-1])
        def key(n: str) -> tuple:
            pkg = "/".join(n.split("/")[:-1])
            level = session.infer_architectural_level(n)
            return (
                0 if level == ref_level else 1,
                0 if pkg == ref_pkg else 1,
                n,
            )
        return sorted(names, key=key)

    # Used by (who depends on this file) — capped to 3
    try:
        impact = session.query_template("impact_analysis", module=uri)
        if impact:
            all_names = _sort_by_relevance(
                [r.get("name", "?") for r in impact], path)
            tagged = []
            for n in all_names[:3]:
                label = _edge_label(session, n, path)
                tagged.append(f"{n} ({label})" if label else n)
            parts.append(f"Used by: {', '.join(tagged)}")
            if len(all_names) > 3:
                parts.append(f"  (+{len(all_names) - 3} more — use query_impact() for full list)")
    except Exception:
        pass

    # Depends on (what this file imports) — capped to 5
    try:
        deps = session.query_template("deps_of", module=uri)
        if deps:
            all_names = _sort_by_relevance(
                [r.get("name", "?") for r in deps], path)
            tagged = []
            for n in all_names[:5]:
                label = _edge_label(session, path, n)
                tagged.append(f"{n} ({label})" if label else n)
            parts.append(f"Depends on: {', '.join(tagged)}")
    except Exception:
        pass

    # Rules
    try:
        rules = session.query_template("rules_zone", module=uri)
        if rules:
            seen: set[str] = set()
            rule_texts: list[str] = []
            for r in rules:
                txt = r.get("rule_text", "")
                if txt and txt not in seen:
                    seen.add(txt)
                    rule_texts.append(txt)
            if rule_texts:
                parts.append(f"Rules: {'; '.join(rule_texts[:3])}")
    except Exception:
        pass

    if not parts:
        return ""

    # Boundary check after 2+ files visited
    if hasattr(session, '_visited_files') and len(session._visited_files) >= 2:
        try:
            boundary = session.get_boundary_status()
            if boundary:
                remaining = boundary.get("remaining_in_scope", [])
                out = boundary.get("out_of_scope_sample", [])
                explored_pct = boundary.get("explored_pct", 0)
                if remaining or out:
                    parts.append(f"[Boundary] {explored_pct}% of impact zone explored.")
                    if remaining:
                        parts.append(f"  Still in scope: {', '.join(remaining[:5])}")
                    if out:
                        parts.append(f"  Out of scope (skip): {', '.join(out[:5])}")
        except Exception:
            pass

    path_display = path.rsplit("/", 1)[-1] if "/" in path else path
    return (
        f"[Synrax Navigation for {path_display}]\n"
        + "\n".join(f"  {p}" for p in parts)
        + "\n  -> Follow 'Used by' files IF they relate to the problem."
        + "\n--- file content below ---\n"
    )


def _build_quick_map(session: Any, package_name: str) -> str:
    """Build a compact initial graph overview for the system prompt.

    Shows most-connected modules (excluding __init__.py hubs).
    """
    files = session.file_count
    triples = session.raw_triple_count
    if files == 0:
        return ""

    try:
        top = session.query(
            "PREFIX arch: <http://archgraph.example.org/> "
            "SELECT ?name (COUNT(?dep) AS ?cnt) WHERE { "
            "  ?dep arch:dependsOn ?m . "
            "  ?m arch:moduleName ?name . "
            "} GROUP BY ?name ?m ORDER BY DESC(?cnt) LIMIT 20"
        )
    except Exception:
        top = []

    filtered = []
    for r in top:
        name = r.get("name", "")
        if name.endswith("__init__.py"):
            continue
        cnt = int(r.get("cnt", "0"))
        if cnt == 0:
            continue
        filtered.append((name, cnt))
        if len(filtered) >= 8:
            break

    if not filtered:
        return f"[Synrax Graph] {files} modules, {triples} raw triples — no high-degree nodes."

    lines = [f"[Synrax Graph] {files} modules, {triples} raw triples. Most-connected:"]
    for name, cnt in filtered:
        lines.append(f"  {name} (imported by {cnt} modules)")
    return "\n".join(lines)


class ToolSandbox:
    """Executes tool calls against a real codebase directory.

    In 'raw' mode: only filesystem tools (list_dir, read_file, grep, find).
    In 'synrax' mode: filesystem tools + REAL Synrax runtime (SessionGraph + OWL reasoning)
        + [Synrax Navigation] blocks injected into read_file results (Double Helix).

    Tracks stats: files read, tool calls, chars returned.
    """

    def __init__(
        self,
        project_root: Path,
        package_dir: Path,
        package_name: str,
        mode: str = "raw",
        session_graph: Any = None,
    ):
        self.project_root = project_root.resolve()
        self.package_dir = package_dir.resolve()
        self.package_name = package_name
        self.mode = mode  # "raw" or "synrax"

        # Real Synrax runtime (only for synrax mode)
        self._session = session_graph
        self._synrax_tools: dict[str, Any] = {}
        if mode == "synrax" and session_graph is not None:
            from synrax.runtime.tools import make_synrax_tools
            self._synrax_tools = make_synrax_tools(session_graph)
            # Reset visited files per-question so tension/boundary track fresh
            session_graph._visited_files = set()

        # Double Helix: read cache (dedup repeated file reads)
        self._read_cache: dict[str, str] = {}
        # Tension alert tracking
        self._reads_since_alert = 0

        # Stats
        self.tool_calls = 0
        self.files_read: set[str] = set()
        self.total_output_chars = 0
        self.synrax_calls = 0

    def get_tools_schema(self) -> list[dict[str, Any]]:
        """Return OpenAI-format tool definitions."""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": (
                        f"List files and subdirectories in a directory relative to the "
                        f"{self.package_name} package root. Use '' or '.' for the root."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative directory path (e.g., '' for root, 'utils/' for a subdir)",
                            },
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": (
                        f"Read the contents of a Python file in the {self.package_name} package. "
                        f"Returns the first {MAX_FILE_CHARS} characters. Use start_line/end_line to read specific sections."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative file path (e.g., 'core.py', 'utils/helpers.py')",
                            },
                            "start_line": {
                                "type": "integer",
                                "description": "Start line (1-based, optional)",
                            },
                            "end_line": {
                                "type": "integer",
                                "description": "End line (1-based, optional)",
                            },
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grep_search",
                    "description": (
                        f"Search for a text pattern across all .py files in the {self.package_name} package. "
                        f"Returns matching lines with file paths and line numbers. Case-insensitive."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Text or regex pattern to search for",
                            },
                        },
                        "required": ["pattern"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "find_files",
                    "description": (
                        f"Find files matching a glob pattern in the {self.package_name} package."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Glob pattern (e.g., '*.py', '**/test_*.py', 'core*')",
                            },
                        },
                        "required": ["pattern"],
                    },
                },
            },
        ]

        if self.mode == "synrax":
            tools.extend([
                {
                    "type": "function",
                    "function": {
                        "name": "query_impact",
                        "description": (
                            "Synrax runtime: get all files affected if a module changes. "
                            "Uses OWL reasoning to compute transitive blast radius with provenance "
                            "(structural from AST imports, annotated from CodeDNA, inferred from OWL)."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "module_path": {
                                    "type": "string",
                                    "description": f"Module file path (e.g., '{self.package_name}/core.py')",
                                },
                            },
                            "required": ["module_path"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_deps",
                        "description": (
                            "Synrax runtime: get all direct and transitive dependencies of a module. "
                            "Computed from AST import analysis + OWL reasoning."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "module_path": {
                                    "type": "string",
                                    "description": f"Module file path (e.g., '{self.package_name}/core.py')",
                                },
                            },
                            "required": ["module_path"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_graph_status",
                        "description": (
                            "Synrax runtime: get graph stats — triple count, files ingested, "
                            "orphan modules, circular dependencies detected by OWL reasoning."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_rules",
                        "description": (
                            "Synrax runtime: get architectural rules for a module and its impact zone. "
                            "Returns CodeDNA-annotated rules (if any) for the module and affected modules."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "module_path": {
                                    "type": "string",
                                    "description": f"Module file path (e.g., '{self.package_name}/core.py')",
                                },
                            },
                            "required": ["module_path"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_boundary",
                        "description": (
                            "Synrax runtime: show exploration boundary — what percentage of the "
                            "impact zone you've explored, remaining in-scope files, and out-of-scope "
                            "files to skip. Call this to decide if you need to read more files."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_tension",
                        "description": (
                            "Synrax runtime: show how much of the dependency blast zone remains "
                            "unexplored. Returns tension ratio, high-impact unvisited files, and "
                            "coverage advice. Call before finalizing your answer."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                },
            ])

        return tools

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        """Execute a tool call and return the result string."""
        self.tool_calls += 1

        try:
            # Filesystem tools (available in both modes)
            if name == "list_directory":
                return self._list_directory(arguments.get("path", ""))
            elif name == "read_file":
                return self._read_file(
                    arguments.get("path", ""),
                    arguments.get("start_line"),
                    arguments.get("end_line"),
                )
            elif name == "grep_search":
                return self._grep_search(arguments.get("pattern", ""))
            elif name == "find_files":
                return self._find_files(arguments.get("pattern", "*.py"))

            # Synrax runtime tools (real SessionGraph + OWL reasoning)
            elif name in self._synrax_tools:
                self.synrax_calls += 1
                fn = self._synrax_tools[name]
                # Route arguments: tools with module_path arg vs no-arg tools
                if name in ("query_impact", "query_deps", "query_rules"):
                    result = fn(arguments.get("module_path", ""))
                elif name == "query_boundary":
                    result = fn()
                elif name == "query_tension":
                    result = fn()
                else:
                    result = fn()
                self.total_output_chars += len(result)
                return result
            else:
                return f"Unknown tool: {name}"
        except Exception as exc:
            return f"Error: {exc}"

    # -- Filesystem tools --

    def _resolve_path(self, rel: str) -> Path:
        """Resolve a relative path to absolute, constrained to package_dir."""
        rel = rel.strip().strip("/").strip("\\")
        if not rel or rel == ".":
            return self.package_dir
        # Allow both "click/core.py" and "core.py" styles
        candidate = self.package_dir / rel
        if candidate.exists():
            return candidate.resolve()
        # Maybe they used package-prefixed path like "click/core.py"
        if "/" in rel:
            parts = rel.split("/", 1)
            if parts[0] == self.package_name:
                candidate = self.package_dir / parts[1]
                if candidate.exists():
                    return candidate.resolve()
        # Also try project_root-relative
        candidate = self.project_root / rel
        if candidate.exists():
            return candidate.resolve()
        return self.package_dir / rel  # will fail naturally

    def _list_directory(self, path: str) -> str:
        target = self._resolve_path(path)
        if not target.is_dir():
            return f"Not a directory: {path}"
        # Security: must be within project
        try:
            target.relative_to(self.project_root)
        except ValueError:
            return "Access denied: path outside project"

        entries = []
        for child in sorted(target.iterdir()):
            if child.name.startswith((".", "__pycache__")):
                continue
            rel = str(child.relative_to(self.project_root)).replace("\\", "/")
            suffix = "/" if child.is_dir() else ""
            entries.append(f"{rel}{suffix}")

        result = "\n".join(entries) if entries else "(empty directory)"
        self.total_output_chars += len(result)
        return result

    def _read_file(self, path: str, start_line: int | None = None, end_line: int | None = None) -> str:
        target = self._resolve_path(path)
        if not target.is_file():
            return f"File not found: {path}"
        try:
            target.relative_to(self.project_root)
        except ValueError:
            return "Access denied: path outside project"

        rel = str(target.relative_to(self.project_root)).replace("\\", "/")
        self.files_read.add(rel)

        # Double Helix: read cache — on re-read return short cached summary
        if rel in self._read_cache:
            snippet = self._read_cache[rel][:300]
            result = (
                f"[Already read {rel}. Showing first 300 chars — use grep_search to search for specifics.]\n"
                f"{snippet}..."
            )
            self.total_output_chars += len(result)
            return result

        content = target.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines(keepends=True)
        total_lines = len(lines)

        if start_line is not None or end_line is not None:
            sl = max(1, start_line or 1)
            el = min(total_lines, end_line or total_lines)
            lines = lines[sl - 1 : el]
            header = f"[{rel} lines {sl}-{el} of {total_lines}]\n"
        else:
            header = f"[{rel} — {total_lines} lines]\n"

        text = header + "".join(lines)
        if len(text) > MAX_FILE_CHARS:
            text = text[:MAX_FILE_CHARS] + f"\n... (truncated at {MAX_FILE_CHARS} chars, {total_lines} total lines)"

        # Cache the raw content for dedup
        self._read_cache[rel] = text

        # Double Helix: inject [Synrax Navigation] block for .py files in synrax mode
        if self.mode == "synrax" and self._session is not None and rel.endswith(".py"):
            # Auto-ingest + mark visited
            try:
                self._session.ingest_file(rel)
            except Exception:
                pass
            self._session.mark_visited(rel)

            nav = _build_nav_hint(self._session, rel, self.package_name)
            if nav:
                text = nav + text

            self._reads_since_alert += 1

        self.total_output_chars += len(text)
        return text

    def _grep_search(self, pattern: str) -> str:
        if not pattern:
            return "Empty pattern"
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            # Treat as literal
            regex = re.compile(re.escape(pattern), re.IGNORECASE)

        matches = []
        for py_file in sorted(self.package_dir.rglob("*.py")):
            if "__pycache__" in str(py_file):
                continue
            try:
                py_file.relative_to(self.project_root)
            except ValueError:
                continue

            try:
                lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue

            rel = str(py_file.relative_to(self.project_root)).replace("\\", "/")
            for i, line in enumerate(lines, 1):
                if regex.search(line):
                    matches.append(f"{rel}:{i}: {line.rstrip()}")
                    if len(matches) >= 50:
                        break
            if len(matches) >= 50:
                break

        if not matches:
            return f"No matches for '{pattern}'"
        result = "\n".join(matches)
        if len(matches) >= 50:
            result += "\n... (results capped at 50 matches)"
        self.total_output_chars += len(result)
        return result

    def _find_files(self, pattern: str) -> str:
        matches = []
        for f in sorted(self.package_dir.rglob(pattern)):
            if "__pycache__" in str(f):
                continue
            try:
                rel = str(f.relative_to(self.project_root)).replace("\\", "/")
                matches.append(rel)
            except ValueError:
                continue

        result = "\n".join(matches) if matches else f"No files matching '{pattern}'"
        self.total_output_chars += len(result)
        return result

    # -- (Synrax tools are resolved via self._synrax_tools from make_synrax_tools) --

    def check_tension_alert(self) -> str | None:
        """Return a tension alert string if it's time to inject one, else None.

        Called every turn in the agent loop (synrax mode only).
        Fires after every TENSION_ALERT_INTERVAL file reads.
        """
        if self.mode != "synrax" or self._session is None:
            return None
        if self._reads_since_alert < TENSION_ALERT_INTERVAL:
            return None
        self._reads_since_alert = 0
        try:
            tension = self._session.compute_tension()
        except Exception:
            return None
        ratio = tension.get("tension_ratio", 0.0)
        if ratio <= 0.2:
            return None  # coverage is fine, no alert needed
        high = tension.get("high_tension_files", [])
        unvisited = tension.get("blast_zone_unvisited", 0)
        total = tension.get("blast_zone_total", 0)
        lines = [
            f"[Synrax Tension Alert] {round(ratio * 100)}% of blast zone unexplored ({unvisited}/{total} files)."
        ]
        if high:
            lines.append(f"High-impact unvisited files: {', '.join(high)}")
        lines.append("Consider reading these files before finalizing your answer.")
        return "\n".join(lines)

    def get_quick_map(self) -> str:
        """Return a [Synrax Graph] initial map for the system prompt."""
        if self.mode != "synrax" or self._session is None:
            return ""
        return _build_quick_map(self._session, self.package_name)

    def get_stats(self) -> dict[str, Any]:
        return {
            "tool_calls": self.tool_calls,
            "files_read": len(self.files_read),
            "files_read_list": sorted(self.files_read),
            "total_output_chars": self.total_output_chars,
            "synrax_calls": self.synrax_calls,
        }


# ---------------------------------------------------------------------------
# AGENT LOOP — LLM + tool calls
# ---------------------------------------------------------------------------

def call_openrouter(
    model: str,
    messages: list[dict],
    tools: list[dict] | None,
    api_key: str,
    max_tokens: int = 2000,
) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/synrax",
        "X-Title": "Synrax Agent Benchmark",
    }
    payload: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    data_bytes = json.dumps(payload).encode("utf-8")

    t0 = time.monotonic()
    last_err = ""
    for attempt in range(5):
        try:
            req = Request(OPENROUTER_URL, data=data_bytes, headers=headers, method="POST")
            with urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            last_err = f"HTTP {e.code}: {body}"
            if e.code >= 500 or e.code == 429:
                time.sleep(3 ** attempt)
                continue
            return {"error": last_err, "latency_ms": round((time.monotonic() - t0) * 1000)}
        except (URLError, OSError, TimeoutError) as e:
            last_err = f"Network error: {e}"
            time.sleep(3 ** attempt)
            continue
    else:
        return {"error": last_err, "latency_ms": round((time.monotonic() - t0) * 1000)}

    latency = round((time.monotonic() - t0) * 1000)
    usage = data.get("usage", {})
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})

    return {
        "message": msg,
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
        "latency_ms": latency,
        "model": data.get("model", model),
        "finish_reason": choice.get("finish_reason", ""),
    }


def run_agent_loop(
    model: str,
    task: str,
    sandbox: ToolSandbox,
    api_key: str,
) -> dict[str, Any]:
    """Run a full agent loop: LLM navigates codebase via tools until it gives a final answer.

    Returns: {answer, messages, tool_calls, files_read, tokens, latency_ms, turns}
    """
    tools_schema = sandbox.get_tools_schema()

    system_prompt = (
        f"You are an expert software architect analyzing the '{sandbox.package_name}' Python package.\n"
        f"You have access to tools to explore the codebase. Use them to find the answer.\n"
        f"When you have enough information, give your FINAL ANSWER listing all relevant module file paths.\n"
        f"Be thorough: trace ALL dependencies, not just the first level.\n"
        f"Use file paths relative to the project root (e.g., '{sandbox.package_name}/core.py')."
    )

    if sandbox.mode == "synrax":
        quick_map = sandbox.get_quick_map()
        system_prompt = (
            f"You are an expert software architect analyzing the '{sandbox.package_name}' Python package.\n"
            f"Your task: find ALL modules related to the question. Be thorough — trace the full boundary.\n"
            f"Use file paths relative to the project root (e.g., '{sandbox.package_name}/core.py').\n"
            "\n"
            "## Synrax Runtime — Automatic Dependency Analysis (Double Helix)\n"
            "\n"
            "This codebase is instrumented with Synrax ArchGraph. The dependency graph has been\n"
            "pre-built from all CodeDNA annotations and Python import analysis.\n"
            "\n"
            "**IMPORTANT**: Every `read_file()` result for a .py file starts with a `[Synrax Navigation]`\n"
            "block at the TOP — read it FIRST before the file content. This block shows:\n"
            "- **Used by**: files that depend on this file, with relevance labels:\n"
            "  - `(annotated)` = explicitly marked by the developer as a consumer — HIGH relevance\n"
            "  - `(structural)` = connected via import statement — verify relevance before reading\n"
            "- **Depends on**: what this file imports (also labeled)\n"
            "- **Rules**: architectural constraints you must respect\n"
            "- **[Boundary]**: (appears after 2+ files read) shows exploration progress and out-of-scope files\n"
            "\n"
            "You may also receive `[Synrax Tension Alert]` messages mid-conversation when the blast zone\n"
            "has significant unexplored files. These alerts name specific high-impact files you should read.\n"
            "\n"
            "### Tools\n"
            "- **Filesystem**: list_directory, read_file, grep_search, find_files\n"
            "- **Graph**: query_impact, query_deps, query_rules, query_graph_status, query_boundary, query_tension\n"
            "\n"
            "### Strategy\n"
            "1. Start with query_graph_status to see the graph overview\n"
            "2. Use query_impact or query_deps to get complete dependency chains in one call\n"
            "3. READ files — the [Synrax Navigation] block at the TOP tells you where to go next\n"
            "4. Prioritize `(annotated)` files over `(structural)` ones\n"
            "5. SKIP files listed as out-of-scope in the [Boundary] section\n"
            "6. When you receive a [Synrax Tension Alert], read the high-impact files it names\n"
            "7. Call query_tension() before finalizing — target >80% of blast zone explored\n"
            "8. The graph tools include transitive closure — you don't need to manually trace imports\n"
        )
        if quick_map:
            system_prompt += f"\n{quick_map}\n"

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]

    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_latency_ms = 0
    turns = 0

    for _ in range(MAX_TURNS):
        turns += 1
        result = call_openrouter(model, messages, tools_schema, api_key)

        if result.get("error"):
            return {
                "answer": "",
                "error": result["error"],
                "turns": turns,
                "total_tokens": total_prompt_tokens + total_completion_tokens,
                "latency_ms": total_latency_ms,
                **sandbox.get_stats(),
            }

        total_prompt_tokens += result["prompt_tokens"]
        total_completion_tokens += result["completion_tokens"]
        total_latency_ms += result["latency_ms"]

        msg = result["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            # No tool calls — this is the final answer
            return {
                "answer": msg.get("content", ""),
                "turns": turns,
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "total_tokens": total_prompt_tokens + total_completion_tokens,
                "latency_ms": total_latency_ms,
                **sandbox.get_stats(),
            }

        # Execute tool calls
        for tc in tool_calls:
            fn = tc.get("function", {})
            fn_name = fn.get("name", "")
            try:
                fn_args = json.loads(fn.get("arguments", "{}"))
            except json.JSONDecodeError:
                fn_args = {}

            tool_result = sandbox.execute(fn_name, fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.get("id", ""),
                "content": tool_result,
            })

            # Print progress indicator
            print(f".", end="", flush=True)

        # Double Helix: inject tension alert after tool calls if due
        alert = sandbox.check_tension_alert()
        if alert:
            messages.append({
                "role": "user",
                "content": alert,
            })

    # Exhausted turns — use last message content as answer
    last_content = ""
    for m in reversed(messages):
        if m.get("role") == "assistant" and m.get("content"):
            last_content = m["content"]
            break

    return {
        "answer": last_content,
        "turns": turns,
        "max_turns_reached": True,
        "prompt_tokens": total_prompt_tokens,
        "completion_tokens": total_completion_tokens,
        "total_tokens": total_prompt_tokens + total_completion_tokens,
        "latency_ms": total_latency_ms,
        **sandbox.get_stats(),
    }


# ---------------------------------------------------------------------------
# EVALUATION — F1, Precision, Recall, Pass@1
# ---------------------------------------------------------------------------

def extract_modules_from_response(response: str, package_name: str) -> set[str]:
    """Extract module file paths from an LLM response.

    Recognizes patterns like:
      - click/core.py
      - `click/core.py`
      - click.core
      - core.py (within click context)
    """
    found: set[str] = set()
    if not response:
        return found

    # Pattern 1: explicit file paths (package/module.py)
    for m in re.finditer(rf'{re.escape(package_name)}/[\w/]+\.py', response):
        found.add(m.group(0))

    # Pattern 2: dotted module names (click.core → click/core.py)
    for m in re.finditer(rf'{re.escape(package_name)}\.[\w.]+', response):
        path = m.group(0).replace(".", "/") + ".py"
        found.add(path)

    # Pattern 3: bare filenames mentioned (core.py) — map to package/core.py
    for m in re.finditer(r'\b(\w+\.py)\b', response):
        fname = m.group(1)
        if fname == "__init__.py":
            continue
        candidate = f"{package_name}/{fname}"
        found.add(candidate)

    # Pattern 4: backtick-quoted paths
    for m in re.finditer(r'`([^`]+\.py)`', response):
        path = m.group(1).replace("\\", "/")
        if not path.startswith(package_name + "/"):
            path = package_name + "/" + path.split("/")[-1] if "/" not in path else path
        found.add(path)

    return found


def evaluate(predicted: set[str], ground_truth: set[str], package_name: str) -> dict[str, Any]:
    """Compute F1, Precision, Recall, Pass@1.

    Normalizes paths for comparison (strips package prefix mismatches).
    """
    def normalize(s: set[str]) -> set[str]:
        """Normalize to consistent format: package/module.py"""
        normed: set[str] = set()
        for p in s:
            p = p.replace("\\", "/").strip("`").strip()
            # Remove leading ./ or src/
            p = re.sub(r'^(src/|\./)','', p)
            if not p.endswith(".py"):
                p += ".py"
            if "/" not in p:
                p = f"{package_name}/{p}"
            normed.add(p)
        return normed

    pred_norm = normalize(predicted)
    gt_norm = normalize(ground_truth)

    tp = pred_norm & gt_norm
    fp = pred_norm - gt_norm
    fn = gt_norm - pred_norm

    precision = len(tp) / len(pred_norm) if pred_norm else 0.0
    recall = len(tp) / len(gt_norm) if gt_norm else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    pass_at_1 = 1 if f1 >= PASS_THRESHOLD else 0

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "pass_at_1": pass_at_1,
        "tp": sorted(tp),
        "fp": sorted(fp),
        "fn": sorted(fn),
        "predicted_count": len(pred_norm),
        "ground_truth_count": len(gt_norm),
    }


# ---------------------------------------------------------------------------
# BENCHMARK RUNNER
# ---------------------------------------------------------------------------

def run_benchmark(
    repo_name: str,
    model: str,
    api_key: str,
    project_root: Path,
    package_dir: Path,
    package_name: str,
    graph: dict[str, set[str]],
    questions: list[dict[str, Any]],
    session_graph: Any = None,
) -> list[dict[str, Any]]:
    """Run all questions for one repo, both raw and synrax modes."""

    results = []

    for q in questions:
        row: dict[str, Any] = {
            "id": q["id"],
            "type": q["type"],
            "ground_truth_count": len(q["ground_truth"]),
        }

        for mode in ("raw", "synrax"):
            sandbox = ToolSandbox(
                project_root, package_dir, package_name,
                mode=mode,
                session_graph=session_graph if mode == "synrax" else None,
            )

            label = f"{q['id']}:{mode}"
            print(f"    {label} ", end="", flush=True)

            try:
                agent_result = run_agent_loop(model, q["task"], sandbox, api_key)
            except (KeyboardInterrupt, Exception) as exc:
                print(f" CRASH: {type(exc).__name__}: {exc}")
                row[f"{mode}_error"] = str(exc)
                row[f"{mode}_f1"] = 0.0
                row[f"{mode}_pass"] = 0
                continue

            if agent_result.get("error"):
                print(f" ERROR: {agent_result['error']}")
                row[f"{mode}_error"] = agent_result["error"]
                row[f"{mode}_f1"] = 0.0
                row[f"{mode}_pass"] = 0
                continue

            predicted = extract_modules_from_response(agent_result["answer"], package_name)
            ev = evaluate(predicted, q["ground_truth"], package_name)

            row[f"{mode}_f1"] = ev["f1"]
            row[f"{mode}_precision"] = ev["precision"]
            row[f"{mode}_recall"] = ev["recall"]
            row[f"{mode}_pass"] = ev["pass_at_1"]
            row[f"{mode}_tool_calls"] = agent_result["tool_calls"]
            row[f"{mode}_files_read"] = agent_result["files_read"]
            row[f"{mode}_turns"] = agent_result["turns"]
            row[f"{mode}_tokens"] = agent_result["total_tokens"]
            row[f"{mode}_latency_ms"] = agent_result["latency_ms"]
            row[f"{mode}_tp"] = ev["tp"]
            row[f"{mode}_fp"] = ev["fp"]
            row[f"{mode}_fn"] = ev["fn"]

            p1_str = "PASS" if ev["pass_at_1"] else "FAIL"
            print(
                f" F1={ev['f1']:.0%} P={ev['precision']:.0%} R={ev['recall']:.0%} "
                f"[{p1_str}] calls={agent_result['tool_calls']} "
                f"reads={agent_result['files_read']} "
                f"tok={agent_result['total_tokens']:,}"
            )

        results.append(row)

    return results


# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

def print_summary(repo_name: str, model: str, results: list[dict]) -> dict[str, Any]:
    """Print SWE-bench style summary table."""
    print(f"\n{'═' * 78}")
    print(f"  {repo_name} | {model}")
    print(f"{'═' * 78}")
    print(f"  {'Task':<22s} │ {'Mode':<6s} │ {'F1':>5s} {'P':>5s} {'R':>5s} {'P@1':>4s} │ {'Calls':>5s} {'Reads':>5s} {'Tok':>7s}")
    print(f"  {'─'*22}─┼─{'─'*6}─┼─{'─'*5}─{'─'*5}─{'─'*5}─{'─'*4}─┼─{'─'*5}─{'─'*5}─{'─'*7}")

    for r in results:
        for mode in ("raw", "synrax"):
            f1 = r.get(f"{mode}_f1", 0)
            p = r.get(f"{mode}_precision", 0)
            rc = r.get(f"{mode}_recall", 0)
            p1 = r.get(f"{mode}_pass", 0)
            calls = r.get(f"{mode}_tool_calls", 0)
            reads = r.get(f"{mode}_files_read", 0)
            tok = r.get(f"{mode}_tokens", 0)
            tag = "✓" if p1 else "✗"

            id_label = r["id"] if mode == "raw" else ""
            print(
                f"  {id_label:<22s} │ {mode:<6s} │ {f1:>4.0%} {p:>4.0%} {rc:>4.0%}  {tag:>2s}  │ {calls:>5d} {reads:>5d} {tok:>7,}"
            )
        print(f"  {'─'*22}─┼─{'─'*6}─┼─{'─'*5}─{'─'*5}─{'─'*5}─{'─'*4}─┼─{'─'*5}─{'─'*5}─{'─'*7}")

    # Aggregates
    raw_f1s = [r.get("raw_f1", 0) for r in results]
    sx_f1s = [r.get("synrax_f1", 0) for r in results]
    raw_p1 = sum(r.get("raw_pass", 0) for r in results)
    sx_p1 = sum(r.get("synrax_pass", 0) for r in results)
    raw_calls = sum(r.get("raw_tool_calls", 0) for r in results)
    sx_calls = sum(r.get("synrax_tool_calls", 0) for r in results)
    raw_reads = sum(r.get("raw_files_read", 0) for r in results)
    sx_reads = sum(r.get("synrax_files_read", 0) for r in results)
    raw_tok = sum(r.get("raw_tokens", 0) for r in results)
    sx_tok = sum(r.get("synrax_tokens", 0) for r in results)
    n = len(results)

    avg_raw_f1 = sum(raw_f1s) / n if n else 0
    avg_sx_f1 = sum(sx_f1s) / n if n else 0

    print(f"\n  AGGREGATE ({n} tasks):")
    print(f"  {'':>22s} │ {'':>6s} │ {'F1':>5s} {'P@1':>9s} │ {'Calls':>5s} {'Reads':>5s} {'Tokens':>7s}")
    print(f"  {'':>22s} │ {'raw':<6s} │ {avg_raw_f1:>4.0%} {raw_p1:>4d}/{n:<4d} │ {raw_calls:>5d} {raw_reads:>5d} {raw_tok:>7,}")
    print(f"  {'':>22s} │ {'synrax':<6s} │ {avg_sx_f1:>4.0%} {sx_p1:>4d}/{n:<4d} │ {sx_calls:>5d} {sx_reads:>5d} {sx_tok:>7,}")

    delta_f1 = avg_sx_f1 - avg_raw_f1
    delta_calls = sx_calls - raw_calls
    print(f"\n  Δ Synrax vs Raw:  F1 {delta_f1:+.0%}  |  Pass@1 {sx_p1-raw_p1:+d}  |  Tool calls {delta_calls:+d}")

    return {
        "repo": repo_name,
        "model": model,
        "n_tasks": n,
        "raw_avg_f1": round(avg_raw_f1, 3),
        "synrax_avg_f1": round(avg_sx_f1, 3),
        "raw_pass_at_1": raw_p1,
        "synrax_pass_at_1": sx_p1,
        "raw_total_calls": raw_calls,
        "synrax_total_calls": sx_calls,
        "raw_total_reads": raw_reads,
        "synrax_total_reads": sx_reads,
        "raw_total_tokens": raw_tok,
        "synrax_total_tokens": sx_tok,
        "per_task": results,
    }


# ---------------------------------------------------------------------------
# DRY RUN
# ---------------------------------------------------------------------------

def run_dry_run(
    repo_name: str,
    package_name: str,
    graph: dict[str, set[str]],
    questions: list[dict[str, Any]],
    session_graph: Any = None,
) -> None:
    real = [m for m in graph if not m.endswith("__init__.py")]
    n_edges = sum(len(v) for v in graph.values())
    cycles = _find_cycles(graph)

    print(f"\n  ═══ {repo_name} ═══")
    print(f"  AST Graph: {len(real)} modules, {n_edges} edges, {len(cycles)} cycles")
    if session_graph is not None:
        n_raw = session_graph.raw_triple_count
        n_files = len(session_graph._ingested_files)
        print(f"  Synrax SessionGraph: {n_raw} raw triples, {n_files} files ingested")
    print(f"  Agent tools (raw):    list_directory, read_file, grep_search, find_files")
    print(f"  Agent tools (synrax): + query_impact, query_deps, query_rules, query_graph_status, query_boundary, query_tension")
    print(f"  Double Helix:         [Synrax Navigation] in read_file, tension alerts, read cache, quick map")
    print()

    for q in questions:
        gt = q["ground_truth"]
        print(f"  {q['id']} [{q['type']}]")
        print(f"    Task: {q['task'][:120]}...")
        gt_list = sorted(gt)
        print(f"    Ground truth ({len(gt)} modules): {', '.join(gt_list[:6])}", end="")
        if len(gt_list) > 6:
            print(f" (+{len(gt_list) - 6} more)", end="")
        print("\n")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    global MAX_TURNS
    import argparse

    parser = argparse.ArgumentParser(
        description="SWE-bench style agentic benchmark — raw navigation vs Synrax graph tools"
    )
    parser.add_argument("--repo", choices=list(REPOS.keys()))
    parser.add_argument("--all-repos", action="store_true")
    parser.add_argument("--model", default="deepseek/deepseek-chat-v3-0324")
    parser.add_argument("--all-models", action="store_true")
    parser.add_argument("--output", default="benchmark_agent_results.json")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-turns", type=int, default=MAX_TURNS)
    args = parser.parse_args()

    max_turns_cfg = args.max_turns
    MAX_TURNS = max_turns_cfg

    repo_list: list[tuple[str, dict[str, str]]] = []
    if args.all_repos:
        repo_list = list(REPOS.items())
    elif args.repo:
        repo_list = [(args.repo, REPOS[args.repo])]
    else:
        repo_list = [("click", REPOS["click"])]

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    models = MODELS if args.all_models else [args.model]

    print("=" * 78)
    print("  Synrax Agent Benchmark (SWE-bench style)")
    print(f"  Repos: {', '.join(n for n, _ in repo_list)}")
    if not args.dry_run:
        print(f"  Models: {', '.join(models)}")
        print(f"  Max turns: {MAX_TURNS}")
    print(f"  Metrics: F1, Precision, Recall, Pass@1 (threshold={PASS_THRESHOLD})")
    print("=" * 78)

    all_summaries: list[dict[str, Any]] = []

    for repo_name, config in repo_list:
        print(f"\n  ── Setting up: {repo_name} ──")

        project_root, package_dir = download_repo(repo_name, config)
        package_name = config["package_name"]

        print("  Building dependency graph (AST) ...", end=" ", flush=True)
        graph = build_dep_graph(project_root, package_dir)
        real = [m for m in graph if not m.endswith("__init__.py")]
        n_edges = sum(len(v) for v in graph.values())
        print(f"{len(real)} modules, {n_edges} edges.")

        # Build real Synrax SessionGraph (root = project_root so paths include package prefix)
        print("  Building Synrax SessionGraph (OWL-RL) ...", end=" ", flush=True)
        from synrax.runtime.session_graph import SessionGraph
        sg = SessionGraph(project_root)
        # Ingest only the package dir files (not tests, docs, examples)
        for py_file in sorted(package_dir.rglob("*.py")):
            try:
                rel_parts = py_file.relative_to(package_dir).parts
            except ValueError:
                continue
            if any(p.startswith((".", "__pycache__")) for p in rel_parts[:-1]):
                continue
            sg.ingest_file(py_file)
        n_raw = sg.raw_triple_count
        print(f"{n_raw} raw triples, {len(sg._ingested_files)} files ingested.")

        questions = generate_questions(graph, package_name)
        print(f"  Generated {len(questions)} tasks with computed ground truth.")

        if args.dry_run or not api_key:
            if not api_key and not args.dry_run:
                print(" No OPENROUTER_API_KEY — dry-run mode.")
            run_dry_run(repo_name, package_name, graph, questions, session_graph=sg)
            continue

        for model in models:
            print(f"\n  ═══ {repo_name} × {model} ═══")
            results = run_benchmark(
                repo_name, model, api_key,
                project_root, package_dir, package_name,
                graph, questions, session_graph=sg,
            )
            summary = print_summary(repo_name, model, results)
            all_summaries.append(summary)

    if not all_summaries:
        return

    # Cross-model/repo summary
    if len(all_summaries) > 1:
        print(f"\n{'═' * 78}")
        print("  OVERALL SUMMARY")
        print(f"{'═' * 78}")
        print(f"  {'Repo + Model':<45s} │ {'F1':>5s} {'P@1':>7s} │ {'Calls':>5s} {'Reads':>5s} {'Tokens':>8s}")
        for s in all_summaries:
            label = f"{s['repo']} | {s['model'].split('/')[-1]}"
            raw_lbl = f"  {label:<45s} │ {s['raw_avg_f1']:>4.0%} {s['raw_pass_at_1']}/{s['n_tasks']:<4d} │ {s['raw_total_calls']:>5d} {s['raw_total_reads']:>5d} {s['raw_total_tokens']:>8,}"
            sx_lbl = f"  {'  + synrax':<45s} │ {s['synrax_avg_f1']:>4.0%} {s['synrax_pass_at_1']}/{s['n_tasks']:<4d} │ {s['synrax_total_calls']:>5d} {s['synrax_total_reads']:>5d} {s['synrax_total_tokens']:>8,}"
            print(raw_lbl)
            print(sx_lbl)

    # Save
    output_path = Path(args.output)
    output_data = {
        "benchmark": "synrax_agent_v1",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "pass_threshold": PASS_THRESHOLD,
        "max_turns": MAX_TURNS,
        "repos": [n for n, _ in repo_list],
        "summaries": all_summaries,
    }
    output_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Results saved to: {output_path}")


if __name__ == "__main__":
    main()
