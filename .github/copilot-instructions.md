# Synrax — Project Guidelines

## What This Is

Synrax implements **ArchGraph**: a formal knowledge graph layer for CodeDNA-annotated codebases.
It extracts CodeDNA annotations (YAML + docstrings) into RDF triples, validates them with SHACL shapes,
infers transitive dependencies via OWL reasoning, and exposes a SPARQL endpoint for impact analysis.

Reference specs:
- [ArchGraph Spec](../docs/ArchGraph_Spec.md) — full formal specification
- [CodeDNA Protocol](https://github.com/Larens94/codedna) — upstream annotation standard (v0.7)

## Architecture

```
Source (CodeDNA annotations)
  → Extraction (codedna-export CLI, Python + rdflib)
    → Ontology (OWL schema + SHACL shapes, Oxigraph triplestore)
      → Query (SPARQL endpoint on localhost:7878)
        → Agent Integration (JSON context builder)
```

Key components:
- `synrax/extract/` — CodeDNA parser (`.codedna` YAML + Python docstrings → RDF/Turtle)
- `synrax/schema/` — OWL ontology (`schema.owl`) and SHACL shapes (`shapes.ttl`)
- `synrax/query/` — SPARQL query templates and endpoint wrapper
- `synrax/cli/` — `codedna-export` CLI entry point

## Tech Stack

- **Language:** Python 3.11+
- **RDF:** rdflib (serialization), oxigraph (triplestore/SPARQL)
- **OWL reasoning:** owlrl (OWL-RL profile, pure Python)
- **SHACL validation:** pyshacl
- **CLI:** click
- **Testing:** pytest
- **Packaging:** pyproject.toml (PEP 621)

## Code Style

- Type hints on all public functions
- Docstrings follow CodeDNA Level 1/2 format (this project dogfoods the protocol)
- Use `pathlib.Path` for all file paths, never raw strings
- RDF namespaces defined once in `synrax/namespaces.py`

## Build & Test

```bash
pip install -e ".[dev]"       # install with dev deps
pytest                        # run all tests
pytest -x --tb=short          # quick fail-fast mode
codedna-export --help         # CLI entry point
```

## Conventions

- All RDF output uses Turtle format (`.ttl`)
- SPARQL queries stored as `.rq` files in `synrax/query/templates/`
- OWL ontology prefix: `arch:` → `http://archgraph.example.org/`
- SHACL shapes use `sh:` standard prefix
- Validation reports: JSON format with `conforms`, `violations[]`, `summary`
- CLI exits 0 on success, 1 on validation failure, 2 on parse error
