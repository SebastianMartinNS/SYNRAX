"""synrax/schema/ — OWL ontology and SHACL shapes for ArchGraph.

exports: load_schema() -> Graph | load_shapes() -> Graph | reason(graph) -> Graph | validate(graph) -> Report
used_by: synrax/extract/pipeline.py → post-extraction validation | synrax/cli/main.py → validate command
rules:   schema.owl and shapes.ttl MUST be kept in sync with ArchGraph spec.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial package scaffold.
"""

from synrax.schema.loader import load_schema, load_shapes
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate

__all__ = ["load_schema", "load_shapes", "reason", "validate"]
