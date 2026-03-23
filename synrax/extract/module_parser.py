"""synrax/extract/module_parser.py — Python module docstring parser → RDF triples.

exports: parse_module(path, project) -> Graph
used_by: synrax/extract/pipeline.py → extract_codebase
rules:   Uses AST to extract module-level and function-level docstrings.
         Parses CodeDNA fields: exports, used_by, rules, agent.
         Sentence splitting on '.' for rules.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial module parser with Level 1 + Level 2.
"""

from __future__ import annotations

import ast
import logging
import re
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.namespaces import ARCH, RDF, RDFS, bind_namespaces

log = logging.getLogger(__name__)


def _make_module_uri(module_path: str) -> str:
    """Create a URI-safe identifier from a module file path."""
    return module_path.replace("/", "_").replace("\\", "_").replace(".py", "").replace("-", "_")


def _parse_codedna_fields(docstring: str) -> dict[str, str]:
    """Extract CodeDNA fields from a docstring.

    Recognized fields: exports, used_by, rules, agent.
    Each field starts with 'fieldname:' and continues until the next field or end.
    """
    fields: dict[str, str] = {}
    field_pattern = re.compile(
        r"^(exports|used_by|rules|agent|deps|purpose):\s*(.+?)(?=\n(?:exports|used_by|rules|agent|deps|purpose):|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for match in field_pattern.finditer(docstring):
        key = match.group(1).strip()
        value = match.group(2).strip()
        # Normalize multi-line continuations
        value = re.sub(r"\n\s+", " ", value)
        fields[key] = value
    return fields


def _parse_exports(exports_str: str) -> list[dict[str, str]]:
    """Parse 'exports:' field into list of {name, signature}."""
    results = []
    for part in exports_str.split("|"):
        # Further split on commas to handle "Cast, Coalesce" style exports
        sub_parts = [s.strip() for s in part.split(",")]
        for sub in sub_parts:
            if not sub:
                continue
            # Match: func_name(args) -> return_type  or  func_name() → type
            m = re.match(r"(\w+)\(([^)]*)\)\s*(?:->|→)\s*(.+)", sub)
            if m:
                results.append({
                    "name": m.group(1),
                    "signature": f"({m.group(2)}) -> {m.group(3).strip()}",
                })
            elif sub:
                name = sub.split("(")[0].strip()
                if name.isidentifier():
                    results.append({"name": name, "signature": ""})
    return results


_USED_BY_SENTINELS = frozenset({"none", "unknown", "n/a", "na", "internal", "self"})


def _parse_used_by(used_by_str: str) -> list[dict[str, str | bool]]:
    """Parse 'used_by:' field into list of {module, function, cascade}."""
    results = []
    for part in used_by_str.split("|"):
        # Further split on commas to handle "aggregates.py → X, base.py → Y"
        sub_parts = [s.strip() for s in part.split(",")]
        for sub in sub_parts:
            if not sub:
                continue
            # Skip sentinel / placeholder values (but log it)
            if sub.lower() in _USED_BY_SENTINELS:
                log.debug("Skipping used_by sentinel: %r", sub)
                continue
            cascade = "[cascade]" in sub
            sub = sub.replace("[cascade]", "").strip()

            # Match: module.py -> function_name  or  module.py → function_name
            m = re.match(r"([\w/._-]+)\s*(?:->|→)\s*(\w+)", sub)
            if m:
                mod = m.group(1).strip()
                func = m.group(2).strip()
                # Skip if the function part is a sentinel
                if func.lower() in _USED_BY_SENTINELS:
                    func = ""
                results.append({"module": mod, "function": func, "cascade": cascade})
            elif sub and " " not in sub:
                # Only treat as module ref if it looks like a path (no spaces)
                results.append({"module": sub, "function": "", "cascade": cascade})
    return results


def _parse_agent(agent_str: str) -> list[dict[str, str]]:
    """Parse 'agent:' field into list of session records.

    Format: model | provider | date | narrative
    """
    results = []
    for line in agent_str.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            results.append({
                "model": parts[0],
                "provider": parts[1],
                "date": parts[2],
                "narrative": parts[3],
            })
    return results


def _parse_rules(rules_str: str) -> list[str]:
    """Split rules text into individual rule sentences."""
    rules = []
    for sentence in re.split(r"\.\s+", rules_str):
        sentence = sentence.strip().rstrip(".")
        if sentence:
            rules.append(sentence)
    return rules


def parse_module(path: Path, project: str = "", root: Path | None = None) -> Graph:
    """Parse a Python module's CodeDNA annotations into RDF triples.

    Args:
        path: Path to the .py source file.
        project: Project name (for URI prefixing).
        root: Codebase root directory. If given, module URIs use relative paths.

    Returns:
        Graph with Module, Export, Rule, and AgentSession triples.
    """
    g = Graph()
    bind_namespaces(g)

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    if root is not None:
        module_path = str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    else:
        module_path = str(path).replace("\\", "/")
    module_uri_name = _make_module_uri(module_path)
    module_uri = ARCH[module_uri_name]

    # --- Level 1: Module docstring ---
    module_docstring = ast.get_docstring(tree)
    if not module_docstring:
        return g

    fields = _parse_codedna_fields(module_docstring)
    if not fields:
        return g

    # Extract purpose from first line (before fields)
    first_line = module_docstring.split("\n")[0]
    purpose_match = re.match(r".*?—\s*(.+?)\.?\s*$", first_line)
    purpose = purpose_match.group(1) if purpose_match else first_line.strip()

    g.add((module_uri, RDF.type, ARCH.Module))
    g.add((module_uri, ARCH.moduleName, Literal(module_path, datatype=XSD.string)))
    g.add((module_uri, ARCH.purpose, Literal(purpose, datatype=XSD.string)))

    # Exports
    for export in _parse_exports(fields.get("exports", "")):
        export_uri = ARCH[f"{module_uri_name}_{export['name']}"]
        g.add((export_uri, RDF.type, ARCH.Export))
        g.add((export_uri, ARCH.exportName, Literal(export["name"], datatype=XSD.string)))
        if export["signature"]:
            g.add((export_uri, ARCH.signature, Literal(export["signature"], datatype=XSD.string)))
        g.add((module_uri, ARCH.exports, export_uri))

    # Used_by → dependsOn triples (inverse) from annotations
    annotation_deps = _parse_used_by(fields.get("used_by", ""))
    annotation_dep_modules: set[str] = set()
    for dep in annotation_deps:
        dep_module_uri = ARCH[_make_module_uri(dep["module"])]
        annotation_dep_modules.add(dep["module"])
        if dep["cascade"]:
            g.add((dep_module_uri, ARCH.cascades, module_uri))
        else:
            g.add((dep_module_uri, ARCH.dependsOn, module_uri))

    # Import-based dependsOn triples (ground truth from AST)
    import_results: list[dict[str, str]] = []
    if root is not None:
        from synrax.extract.import_analyzer import analyze_imports
        import_results = analyze_imports(path, root)
        for imp in import_results:
            imp_uri = ARCH[_make_module_uri(imp["module"])]
            # Import analysis creates forward edges (this file depends on imported file)
            g.add((module_uri, ARCH.dependsOn, imp_uri))

    # Log sentinel used_by values
    raw_used_by = fields.get("used_by", "").strip().lower()
    if raw_used_by in _USED_BY_SENTINELS and not annotation_deps:
        log.info("Module %s has used_by sentinel '%s'", module_path, raw_used_by)

    # Rules
    for idx, rule_text in enumerate(_parse_rules(fields.get("rules", "")), start=1):
        rule_uri = ARCH[f"{module_uri_name}_rule_{idx}"]
        g.add((rule_uri, RDF.type, ARCH.Rule))
        g.add((rule_uri, ARCH.content, Literal(rule_text, datatype=XSD.string)))
        g.add((rule_uri, ARCH.severity, Literal("CRITICAL", datatype=XSD.string)))
        g.add((module_uri, ARCH.hasRule, rule_uri))

    # Agent sessions
    for session in _parse_agent(fields.get("agent", "")):
        session_id = f"session_{session['date'].replace('-', '_')}_{session['model'].replace('-', '_').replace('.', '_')}"
        session_uri = ARCH[session_id]
        agent_uri = ARCH[f"agent_{session['model'].replace('-', '_').replace('.', '_')}"]

        g.add((session_uri, RDF.type, ARCH.AgentSession))
        g.add((session_uri, ARCH.sessionDate, Literal(session["date"], datatype=XSD.date)))
        g.add((session_uri, ARCH.narrative, Literal(session["narrative"], datatype=XSD.string)))
        g.add((session_uri, ARCH.belongs, agent_uri))
        g.add((session_uri, ARCH.visited, module_uri))

        g.add((agent_uri, RDF.type, ARCH.Agent))
        g.add((agent_uri, ARCH.agentModel, Literal(session["model"], datatype=XSD.string)))
        g.add((agent_uri, ARCH.agentProvider, Literal(session["provider"], datatype=XSD.string)))

        g.add((module_uri, ARCH.modifiedBy, session_uri))

    # --- Level 2: Function docstrings ---
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_docstring = ast.get_docstring(node)
            if not func_docstring:
                continue

            func_fields = _parse_codedna_fields(func_docstring)
            rules_text = func_fields.get("rules", "")
            if not rules_text:
                # Also check for "Rules:" in freeform docstring
                rules_match = re.search(
                    r"Rules?:\s*(.+?)(?=\n\s*\n|\Z)", func_docstring, re.DOTALL
                )
                if rules_match:
                    rules_text = rules_match.group(1)

            if not rules_text:
                continue

            func_uri = ARCH[f"{module_uri_name}_{node.name}"]
            g.add((func_uri, RDF.type, ARCH.Function))
            g.add((func_uri, RDFS.label, Literal(node.name, datatype=XSD.string)))
            g.add((func_uri, ARCH.definedIn, module_uri))

            for idx, rule_text in enumerate(_parse_rules(rules_text), start=1):
                rule_uri = ARCH[f"func_rule_{module_uri_name}_{node.name}_{idx}"]
                g.add((rule_uri, RDF.type, ARCH.Rule))
                g.add((rule_uri, ARCH.content, Literal(rule_text, datatype=XSD.string)))
                g.add((rule_uri, ARCH.severity, Literal("HIGH", datatype=XSD.string)))
                g.add((func_uri, ARCH.hasRule, rule_uri))
                g.add((rule_uri, ARCH.appliesTo, func_uri))

    return g
