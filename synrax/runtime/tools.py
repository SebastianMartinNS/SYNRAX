"""synrax/runtime/tools.py — Agent-callable tool functions backed by SessionGraph.

exports: make_synrax_tools(session) -> dict[str, Callable]
used_by: benchmark_agent/swebench/run_agent_multi.py → make_fns | synrax/cli/main.py → serve
rules:   All tool functions return plain strings. No exceptions bubble to the agent.
"""

from __future__ import annotations

from collections.abc import Callable

from synrax.namespaces import make_module_uri, uri_to_path
from synrax.runtime.session_graph import SessionGraph

# Keep backward-compatible alias
_module_uri_fragment = make_module_uri


def make_synrax_tools(session: SessionGraph) -> dict[str, Callable[..., str]]:
    """Create the 5 agent-callable tool functions backed by a SessionGraph.

    Returns:
        Dict mapping tool name → callable.
    """

    def query_impact(module_path: str, **_kw: str) -> str:
        """Find all files transitively affected if this module changes."""
        uri = _module_uri_fragment(module_path)

        # Auto-ingest the queried file if not already
        session.ingest_file(module_path)

        try:
            results = session.query_template("impact_analysis", module=uri)
        except Exception as e:
            return f"Error running impact analysis: {e}"

        if not results:
            return (
                f"No files found that depend on {module_path}.\n"
                f"Graph has {session.file_count} files ingested. "
                f"The module may be a leaf or not yet connected."
            )

        # Classify direct vs transitive
        direct_deps = set()
        try:
            direct_results = session.query(
                "PREFIX arch: <http://archgraph.example.org/> "
                "SELECT DISTINCT ?name WHERE { "
                f"  ?m arch:dependsOn arch:{uri} . "
                "  ?m arch:moduleName ?name . "
                "  FILTER NOT EXISTS { "
                "    ?m arch:dependsOn ?mid . "
                f"    ?mid arch:dependsOn arch:{uri} . "
                f"    FILTER(?mid != arch:{uri}) "
                "  } "
                "}"
            )
            direct_deps = {r.get("name", "") for r in direct_results}
        except Exception:
            pass

        lines = [f"If {module_path} changes, these files are affected:"]
        for r in results:
            name = r.get("name", "?")
            label = "direct" if name in direct_deps else "transitive"
            # EXP-5: Add provenance label (structural/annotated/inferred)
            source = session.get_edge_source(name, uri_to_path(uri))
            if source == "unknown":
                # Try reverse lookup
                source = session.get_edge_source(
                    name,
                    uri_to_path(uri),
                )
            lines.append(f"  - {name} ({label}, {source})")

        direct_count = sum(1 for r in results if r.get("name", "") in direct_deps)
        trans_count = len(results) - direct_count
        lines.append(
            f"[{len(results)} files total, {direct_count} direct, {trans_count} transitive]"
        )
        return "\n".join(lines)

    def query_deps(module_path: str, **_kw: str) -> str:
        """Find all files this module depends on."""
        uri = _module_uri_fragment(module_path)

        session.ingest_file(module_path)

        try:
            results = session.query_template("deps_of", module=uri)
        except Exception as e:
            return f"Error running dependency query: {e}"

        if not results:
            return (
                f"{module_path} has no known dependencies.\n"
                f"It may be a root module or its imports haven't been ingested yet."
            )

        lines = [f"{module_path} depends on:"]
        for r in results:
            name = r.get("name", "?")
            lines.append(f"  - {name}")
        lines.append(f"[{len(results)} dependencies]")
        return "\n".join(lines)

    def query_rules(module_path: str, **_kw: str) -> str:
        """Get architectural rules for this module and its impact zone."""
        uri = _module_uri_fragment(module_path)

        session.ingest_file(module_path)

        try:
            results = session.query_template("rules_zone", module=uri)
        except Exception as e:
            return f"Error querying rules: {e}"

        if not results:
            return f"No architectural rules found for {module_path} or its dependents."

        lines = [f"Rules for {module_path} and its impact zone:"]
        seen: set[str] = set()
        for r in results:
            mod = r.get("module_name", "?")
            rule = r.get("rule_text", "?")
            key = f"{mod}:{rule}"
            if key not in seen:
                seen.add(key)
                lines.append(f"  [{mod}] {rule}")

        return "\n".join(lines)

    def query_graph_status(**_kw: str) -> str:
        """Show current knowledge graph status."""
        raw = session.raw_triple_count
        files = session.file_count

        # Get reasoned count (triggers reasoning if dirty)
        session.ensure_reasoned()
        reasoned = session.reasoned_triple_count
        inferred = reasoned - raw

        lines = [
            f"Graph: {reasoned} triples ({raw} raw + {inferred} inferred), {files} files ingested"
        ]

        # Orphan modules
        try:
            orphans = session.query_template("unused_modules")
            if orphans:
                orphan_names = [r.get("name", "?") for r in orphans[:5]]
                lines.append(f"Orphan modules: {len(orphans)} ({', '.join(orphan_names)})")
            else:
                lines.append("Orphan modules: none")
        except Exception:
            pass

        # Circular deps
        try:
            cycles = session.query_template("circular_deps")
            if cycles:
                lines.append(f"Circular dependencies: {len(cycles)} detected")
            else:
                lines.append("Circular dependencies: none detected")
        except Exception:
            pass

        return "\n".join(lines)

    def query_boundary(**_kw: str) -> str:
        """Show exploration boundary status: what's in scope, what's out, what's remaining."""
        if not hasattr(session, "_visited_files") or not session._visited_files:
            return "No files visited yet. Start reading files to build the impact zone."

        try:
            status = session.get_boundary_status()
        except Exception as e:
            return f"Error computing boundary: {e}"

        if not status:
            return "Boundary analysis not available (no visited files)."

        pct = status.get("explored_pct", 0)
        remaining = status.get("remaining_in_scope", [])
        out = status.get("out_of_scope_sample", [])

        lines = [f"Impact zone exploration: {pct}% complete"]
        lines.append(f"Files visited: {len(session._visited_files)}")
        if remaining:
            lines.append(f"Still in scope ({len(remaining)}): {', '.join(remaining[:8])}")
        else:
            lines.append("All in-scope files have been visited!")
        if out:
            lines.append(f"Out of scope (skip these): {', '.join(out[:8])}")

        return "\n".join(lines)

    def query_tension(**_kw: str) -> str:
        """Show tension level: how much of the dependency blast zone remains unexplored."""
        try:
            tension = session.compute_tension()
        except Exception as e:
            return f"Error computing tension: {e}"

        total = tension.get("blast_zone_total", 0)
        unvisited = tension.get("blast_zone_unvisited", 0)
        ratio = tension.get("tension_ratio", 0.0)
        high = tension.get("high_tension_files", [])
        pct = tension.get("explored_pct", 0)

        if total == 0:
            return "No dependency data available. Read some files first."

        lines = [
            f"Tension: {round(ratio * 100)}% of blast zone unexplored ({unvisited}/{total} files)"
        ]
        lines.append(f"Explored: {pct}%")
        if high:
            lines.append(f"High-impact unvisited: {', '.join(high)}")
        if ratio <= 0.2:
            lines.append("Coverage is good — consider finalizing your answer.")
        elif ratio >= 0.5:
            lines.append("Coverage is low — keep reading files before concluding.")
        return "\n".join(lines)

    return {
        "query_impact": query_impact,
        "query_deps": query_deps,
        "query_rules": query_rules,
        "query_graph_status": query_graph_status,
        "query_boundary": query_boundary,
        "query_tension": query_tension,
    }
