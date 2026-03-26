"""synrax/schema/validator.py — SHACL validation of ArchGraph RDF graphs.

exports: validate(graph, shapes_extensions) -> dict
used_by: synrax/cli/main.py → validate command | synrax/schema/__init__.py
rules:   Returns JSON report with conforms, violations, warnings, statistics.
         Uses pyshacl against bundled shapes.ttl + optional extension shapes.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial SHACL validator.
         claude-opus-4 | anthropic | 2026-03-22 | Dynamic shapes extension support.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from pathlib import Path

from pyshacl import validate as shacl_validate
from rdflib import Graph

from synrax.namespaces import SH
from synrax.schema.loader import load_shapes


def validate(graph: Graph, shapes_extensions: list[Path] | None = None) -> dict:
    """Validate an RDF graph against ArchGraph SHACL shapes.

    Args:
        graph: RDF graph to validate.
        shapes_extensions: Additional SHACL TTL files to merge.

    Returns:
        Validation report dict with keys: conforms, violations, warnings, statistics.
    """
    shapes_graph = load_shapes(extra=shapes_extensions)

    start = time.monotonic()
    conforms, results_graph, results_text = shacl_validate(
        data_graph=graph,
        shacl_graph=shapes_graph,
        inference="none",
        abort_on_first=False,
    )
    elapsed_ms = round((time.monotonic() - start) * 1000)

    violations = []
    warnings = []

    for result in results_graph.subjects(predicate=None, object=SH.ValidationResult):
        record = _extract_result(results_graph, result)
        severity = record.get("severity", "")
        if "Warning" in severity:
            warnings.append(record)
        else:
            violations.append(record)

    # Also parse from standard SHACL result triples
    for _s, _p, o in results_graph.triples((None, SH.result, None)):
        record = _extract_result(results_graph, o)
        severity = record.get("severity", "")
        if record not in violations and record not in warnings:
            if "Warning" in severity:
                warnings.append(record)
            else:
                violations.append(record)

    return {
        "conforms": conforms,
        "violations": violations,
        "warnings": warnings,
        "statistics": {
            "violations_count": len(violations),
            "warnings_count": len(warnings),
            "timestamp": datetime.now(UTC).isoformat(),
            "validator_time_ms": elapsed_ms,
        },
    }


def _extract_result(results_graph: Graph, result_node) -> dict:
    """Extract a single SHACL validation result into a dict."""
    record: dict[str, str] = {}

    for pred, key in [
        (SH.focusNode, "focusNode"),
        (SH.resultPath, "resultPath"),
        (SH.resultMessage, "resultMessage"),
        (SH.resultSeverity, "severity"),
        (SH.sourceShape, "sourceShape"),
        (SH.sourceConstraintComponent, "sourceConstraint"),
    ]:
        for _, _, obj in results_graph.triples((result_node, pred, None)):
            record[key] = str(obj)
            break

    return record
