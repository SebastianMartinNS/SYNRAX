"""synrax — ArchGraph: formal knowledge graph layer for CodeDNA-annotated codebases.

exports: extract_codebase, validate, run_query
used_by: synrax/cli/main.py → CLI entry point
rules:   All public API surfaces through this package root.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial project scaffold.
"""

__version__ = "0.2.0"

from synrax.extract.pipeline import extract_codebase
from synrax.schema.validator import validate
from synrax.query.engine import run_query

__all__ = ["extract_codebase", "validate", "run_query", "__version__"]
