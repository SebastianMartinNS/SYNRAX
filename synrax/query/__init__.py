"""synrax/query/ — SPARQL query templates and endpoint wrapper.

exports: run_query(name, params) -> list[dict] | list_templates() -> list[str]
used_by: synrax/cli/main.py → query command
rules:   Queries stored as .rq files in templates/. Never inline SPARQL strings.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial package scaffold.
"""

from synrax.query.engine import run_query
from synrax.query.templates_loader import list_templates

__all__ = ["run_query", "list_templates"]
