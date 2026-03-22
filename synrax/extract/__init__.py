"""synrax/extract/ — CodeDNA annotation parser and RDF serializer.

exports: parse_manifest(path) -> Graph | parse_module(path) -> Graph | extract_codebase(root) -> Graph
used_by: synrax/cli/main.py → codedna-export command
rules:   Parser validates all 4 CodeDNA fields (exports, used_by, rules, agent).
         Output is always valid RDF/Turtle.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial package scaffold.
"""

from synrax.extract.manifest import parse_manifest
from synrax.extract.module_parser import parse_module
from synrax.extract.pipeline import extract_codebase

__all__ = ["parse_manifest", "parse_module", "extract_codebase"]
