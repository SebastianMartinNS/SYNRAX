"""synrax/query/templates_loader.py — Load SPARQL .rq templates.

exports: list_templates() -> list[str] | load_template(name) -> str
used_by: synrax/query/engine.py | synrax/query/__init__.py
rules:   Templates live in synrax/query/templates/*.rq. Never inline SPARQL.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial template loader.
"""

from __future__ import annotations

from pathlib import Path

_TEMPLATES_DIR = Path(__file__).parent / "templates"


def list_templates() -> list[str]:
    """List available SPARQL query template names (without .rq extension)."""
    if not _TEMPLATES_DIR.is_dir():
        return []
    return sorted(p.stem for p in _TEMPLATES_DIR.glob("*.rq"))


def load_template(name: str) -> str:
    """Load a SPARQL query template by name.

    Args:
        name: Template name (without .rq extension).

    Returns:
        SPARQL query string.

    Raises:
        FileNotFoundError: If template does not exist.
    """
    path = _TEMPLATES_DIR / f"{name}.rq"
    if not path.is_file():
        available = ", ".join(list_templates()) or "(none)"
        raise FileNotFoundError(f"Template '{name}' not found. Available: {available}")
    return path.read_text(encoding="utf-8")
