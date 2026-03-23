"""synrax/cli/main.py — codedna-export CLI entry point.

exports: cli (click.Group)
used_by: pyproject.toml → [project.scripts]
rules:   Exit 0 on success, 1 on validation failure, 2 on parse error.
         --schema and --shapes accept extra OWL/TTL files for project-specific extensions.
         Auto-discovers extensions from .codedna manifest 'extensions' field.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial CLI with export/validate/query commands.
         claude-opus-4 | anthropic | 2026-03-22 | Dynamic schema/shapes extension support.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from synrax.extract import extract_codebase
from synrax.schema import discover_extensions, reason, validate


@click.group()
@click.version_option(package_name="synrax")
def cli() -> None:
    """codedna-export — ArchGraph extraction, validation, and query tool."""


@cli.command()
@click.argument("root", type=click.Path(exists=True, path_type=Path), default=".")
@click.option("-o", "--output", type=click.Path(path_type=Path), default="codebase.ttl")
@click.option("--reason/--no-reason", "apply_reasoning", default=True, help="Run OWL reasoning.")
@click.option("--schema", "extra_schemas", multiple=True, type=click.Path(exists=True, path_type=Path),
              help="Extra OWL/TTL schema files to merge.")
@click.option("--shapes", "extra_shapes", multiple=True, type=click.Path(exists=True, path_type=Path),
              help="Extra SHACL shapes files to merge.")
def export(root: Path, output: Path, apply_reasoning: bool,
           extra_schemas: tuple[Path, ...], extra_shapes: tuple[Path, ...]) -> None:
    """Extract CodeDNA annotations from a codebase into RDF/Turtle."""
    try:
        graph = extract_codebase(root)
    except Exception as exc:
        click.echo(f"Parse error: {exc}", err=True)
        sys.exit(2)

    # Merge CLI-provided extensions with .codedna-discovered ones
    auto_schemas, auto_shapes = discover_extensions(root)
    all_schemas = auto_schemas + list(extra_schemas)
    all_shapes = auto_shapes + list(extra_shapes)

    if all_schemas or all_shapes:
        ext_count = len(all_schemas) + len(all_shapes)
        click.echo(f"Loading {ext_count} extension(s): "
                    f"{len(all_schemas)} schema, {len(all_shapes)} shapes")

    if apply_reasoning:
        graph = reason(graph, schema_extensions=all_schemas or None)

    graph.serialize(destination=str(output), format="turtle")
    click.echo(f"Exported {len(graph)} triples → {output}")


@cli.command()
@click.argument("turtle_file", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output", type=click.Path(path_type=Path), default=None)
@click.option("--shapes", "extra_shapes", multiple=True, type=click.Path(exists=True, path_type=Path),
              help="Extra SHACL shapes files to merge.")
def validate_cmd(turtle_file: Path, output: Path | None, extra_shapes: tuple[Path, ...]) -> None:
    """Validate an RDF graph against ArchGraph SHACL shapes."""
    from rdflib import Graph

    graph = Graph()
    graph.parse(str(turtle_file), format="turtle")

    report = validate(graph, shapes_extensions=list(extra_shapes) or None)

    if output:
        output.write_text(json.dumps(report, indent=2, default=str))
        click.echo(f"Validation report → {output}")
    else:
        click.echo(json.dumps(report, indent=2, default=str))

    if not report.get("conforms", True):
        sys.exit(1)


@cli.command()
@click.argument("query_name")
@click.argument("turtle_file", type=click.Path(exists=True, path_type=Path))
@click.option("-p", "--param", multiple=True, help="Query parameter as key=value.")
def query(query_name: str, turtle_file: Path, param: tuple[str, ...]) -> None:
    """Run a SPARQL query template against an RDF graph."""
    from synrax.query import run_query

    params = dict(p.split("=", 1) for p in param)
    results = run_query(query_name, turtle_file, **params)
    click.echo(json.dumps(results, indent=2, default=str))


@cli.command()
@click.argument("root", type=click.Path(exists=True, path_type=Path), default=".")
@click.option("--pre-ingest", is_flag=True, help="Ingest all .py files on startup.")
def serve(root: Path, pre_ingest: bool) -> None:
    """Start a stdio JSON-RPC server exposing Synrax runtime tools.

    Reads JSON-RPC requests from stdin (one per line), writes responses to stdout.
    Methods: synrax.ingest, synrax.query_impact, synrax.query_deps,
    synrax.query_rules, synrax.status
    """
    from synrax.runtime.session_graph import SessionGraph
    from synrax.runtime.tools import make_synrax_tools

    session = SessionGraph(root)
    tools = make_synrax_tools(session)

    if pre_ingest:
        session.ingest_all()
        click.echo(
            f"Pre-ingested {session.file_count} files, "
            f"{session.raw_triple_count} triples",
            err=True,
        )

    click.echo("synrax serve ready", err=True)

    def _jsonrpc_response(req_id, result):
        return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})

    def _jsonrpc_error(req_id, code, message):
        return json.dumps({"jsonrpc": "2.0", "id": req_id,
                           "error": {"code": code, "message": message}})

    import sys as _sys
    stdin = click.get_text_stream("stdin")
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            click.echo(_jsonrpc_error(None, -32700, "Parse error"))
            continue

        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params", {})

        if method == "synrax.ingest":
            path = params.get("path", "")
            if not path:
                click.echo(_jsonrpc_error(req_id, -32602, "Missing 'path' param"))
                continue
            before = session.raw_triple_count
            session.ingest_file(path)
            added = session.raw_triple_count - before
            click.echo(_jsonrpc_response(req_id, {"triples_added": added}))

        elif method == "synrax.query_impact":
            module = params.get("module", "")
            if not module:
                click.echo(_jsonrpc_error(req_id, -32602, "Missing 'module' param"))
                continue
            result = tools["query_impact"](module_path=module)
            click.echo(_jsonrpc_response(req_id, {"text": result}))

        elif method == "synrax.query_deps":
            module = params.get("module", "")
            if not module:
                click.echo(_jsonrpc_error(req_id, -32602, "Missing 'module' param"))
                continue
            result = tools["query_deps"](module_path=module)
            click.echo(_jsonrpc_response(req_id, {"text": result}))

        elif method == "synrax.query_rules":
            module = params.get("module", "")
            if not module:
                click.echo(_jsonrpc_error(req_id, -32602, "Missing 'module' param"))
                continue
            result = tools["query_rules"](module_path=module)
            click.echo(_jsonrpc_response(req_id, {"text": result}))

        elif method == "synrax.status":
            result = tools["query_graph_status"]()
            click.echo(_jsonrpc_response(req_id, {"text": result}))

        else:
            click.echo(_jsonrpc_error(req_id, -32601, f"Method not found: {method}"))
