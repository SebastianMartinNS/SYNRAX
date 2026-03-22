"""synrax/cli/main.py — codedna-export CLI entry point.

exports: cli (click.Group)
used_by: pyproject.toml → [project.scripts]
rules:   Exit 0 on success, 1 on validation failure, 2 on parse error.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial CLI with export/validate/query commands.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from synrax.extract import extract_codebase
from synrax.schema import reason, validate


@click.group()
@click.version_option(package_name="synrax")
def cli() -> None:
    """codedna-export — ArchGraph extraction, validation, and query tool."""


@cli.command()
@click.argument("root", type=click.Path(exists=True, path_type=Path), default=".")
@click.option("-o", "--output", type=click.Path(path_type=Path), default="codebase.ttl")
@click.option("--reason/--no-reason", "apply_reasoning", default=True, help="Run OWL reasoning.")
def export(root: Path, output: Path, apply_reasoning: bool) -> None:
    """Extract CodeDNA annotations from a codebase into RDF/Turtle."""
    try:
        graph = extract_codebase(root)
    except Exception as exc:
        click.echo(f"Parse error: {exc}", err=True)
        sys.exit(2)

    if apply_reasoning:
        graph = reason(graph)

    graph.serialize(destination=str(output), format="turtle")
    click.echo(f"Exported {len(graph)} triples → {output}")


@cli.command()
@click.argument("turtle_file", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output", type=click.Path(path_type=Path), default=None)
def validate_cmd(turtle_file: Path, output: Path | None) -> None:
    """Validate an RDF graph against ArchGraph SHACL shapes."""
    from rdflib import Graph

    graph = Graph()
    graph.parse(str(turtle_file), format="turtle")

    report = validate(graph)

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
