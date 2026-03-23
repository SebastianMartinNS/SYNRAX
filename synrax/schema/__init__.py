"""synrax/schema/ — OWL ontology and SHACL shapes for ArchGraph.

exports: load_schema(extra) -> Graph | load_shapes(extra) -> Graph | reason(graph) -> Graph | validate(graph) -> Report | discover_extensions(root) -> tuple
used_by: synrax/extract/pipeline.py → post-extraction validation | synrax/cli/main.py → validate command
rules:   schema.owl and shapes.ttl are base layers. Projects extend via .codedna extensions field.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial package scaffold.
         claude-opus-4 | anthropic | 2026-03-22 | Added discover_extensions re-export.
"""

from synrax.schema.loader import discover_extensions, load_schema, load_shapes
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate

__all__ = ["discover_extensions", "load_schema", "load_shapes", "reason", "validate"]
