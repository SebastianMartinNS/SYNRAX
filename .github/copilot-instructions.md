# Synrax — Project Guidelines

## What This Is

Synrax implements **ArchGraph**: a formal knowledge graph layer for CodeDNA-annotated codebases.
It extracts CodeDNA annotations (YAML + docstrings) into RDF triples, validates them with SHACL shapes,
infers transitive dependencies via OWL reasoning, supplements annotations with AST-based import analysis,
and exposes a SPARQL endpoint + runtime JSON-RPC server for impact analysis.

Reference specs:
- [ArchGraph Spec](../docs/ArchGraph_Spec.md) — full formal specification
- [CodeDNA Protocol](https://github.com/Larens94/codedna) — upstream annotation standard (v0.7)

## Architecture

```
Source (CodeDNA annotations + Python AST imports)
  → Extraction (codedna-export CLI, Python + rdflib)
    → Import Analysis (AST-based ground-truth dependency edges)
      → Ontology (OWL schema + SHACL shapes, dynamic extensions)
        → Query (SPARQL templates → JSON)
          → Runtime (SessionGraph + JSON-RPC server for live agent queries)
```

Key components:
- `synrax/extract/` — CodeDNA parser (`.codedna` YAML + Python docstrings → RDF/Turtle)
- `synrax/extract/import_analyzer.py` — AST-based import analysis for ground-truth dependency edges
- `synrax/schema/` — OWL ontology (`schema.owl`), SHACL shapes (`shapes.ttl`), dynamic extension loading
- `synrax/query/` — SPARQL query templates (9 `.rq` files) and engine
- `synrax/runtime/` — `SessionGraph` (incremental lazy-reasoning graph + boundary tracking) + agent tool functions
- `synrax/cli/` — `codedna-export` CLI: export, validate, query, serve commands

## Tech Stack

- **Language:** Python 3.11+
- **RDF:** rdflib (serialization + SPARQL)
- **OWL reasoning:** owlrl (OWL-RL profile, pure Python)
- **SHACL validation:** pyshacl
- **YAML:** PyYAML (manifest + extension discovery)
- **CLI:** click
- **Testing:** pytest (160 tests)
- **Packaging:** pyproject.toml (PEP 621)

## Code Style

- Type hints on all public functions
- Docstrings follow CodeDNA Level 1/2 format (this project dogfoods the protocol)
- Use `pathlib.Path` for all file paths, never raw strings
- RDF namespaces defined once in `synrax/namespaces.py`

## Build & Test

```bash
pip install -e ".[dev]"       # install with dev deps
pytest                        # run all 160 tests
pytest -x --tb=short          # quick fail-fast mode
codedna-export --help         # CLI entry point
codedna-export serve . --pre-ingest  # start runtime server
```

## Conventions

- All RDF output uses Turtle format (`.ttl`)
- SPARQL queries stored as `.rq` files in `synrax/query/templates/`
- OWL ontology prefix: `arch:` → `http://archgraph.example.org/`
- SHACL shapes use `sh:` standard prefix
- Validation reports: JSON format with `conforms`, `violations[]`, `summary`
- CLI exits 0 on success, 1 on validation failure, 2 on parse error
- Base schema is generic; project-specific extensions via `.codedna` `extensions` field or `--schema`/`--shapes` CLI flags
- Runtime tools return plain strings, never raise exceptions to callers
- SessionGraph uses lazy reasoning: OWL-RL only runs when graph is dirty and a query is executed
- SessionGraph tracks visited files for boundary analysis (explored_pct, remaining_in_scope, out_of_scope)
- Runtime tools include boundary tracking (`query_boundary`) and graph status (`query_graph_status`)
