# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML manifests + Python docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL-RL reasoning,
and exposes SPARQL queries for architectural impact analysis.

## Problem

CodeDNA gives you structured annotations in source code. But annotations alone can't answer:

- *"If I modify `db/connection.py`, what breaks?"* — requires transitive dependency tracking
- *"Are there orphan modules nobody depends on?"* — requires global graph analysis
- *"Did the AI agent miss a `[cascade]` target?"* — requires formal enforcement

Synrax turns flat annotations into a **queryable knowledge graph** that answers all of
these with a single SPARQL query each.

## Benchmark Results

Measured on the included 6-module demo codebase (`demo/codebase/`).
Reproducible via `python benchmarks.py`.

| Metric | CodeDNA raw | Synrax (OWL-RL) | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** (4.4×) |
| Dependency edges (`dependsOn`) | 10 | 26 | +16 transitive edges |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| SHACL violations detected | 0 | 37 | from zero |
| SHACL warnings detected | 0 | 11 | from zero |
| SPARQL query templates | 0 | 5 | from zero |
| Node reach (5-node chain) | 1 hop | 4 hops | 4× depth |

**End-to-end pipeline** (6 modules): **< 500 ms**.
Full report: [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md)

## Architecture

```
Source (.codedna manifest + Python docstrings)
  → Extract (Python AST + YAML parser → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties, subproperty propagation)
      → Validate (SHACL shapes → violation/warning report)
        → Query (SPARQL templates → JSON results)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract a codebase → RDF graph (with OWL reasoning)
codedna-export export demo/codebase -o graph.ttl

# Validate the graph against SHACL shapes
codedna-export validate graph.ttl

# Impact analysis: what breaks if db_connection changes?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl

# Detect missed [cascade] targets
codedna-export query cascade_violations graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations found) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/              # CodeDNA annotation parser
│   ├── manifest.py       # .codedna YAML manifest → RDF
│   ├── module_parser.py  # Python docstring (Level 1 + 2) → RDF
│   └── pipeline.py       # Codebase walker + graph merger
├── schema/               # OWL ontology + SHACL validation
│   ├── schema.owl        # ArchGraph OWL ontology (7 classes, transitive/inverse properties)
│   ├── shapes.ttl        # 6 SHACL shapes (completeness, consistency, warnings)
│   ├── reasoner.py       # OWL-RL entailment via owlrl
│   ├── validator.py      # SHACL validation via pyshacl → JSON report
│   └── loader.py         # Schema/shape file loader
├── query/                # SPARQL query engine
│   ├── engine.py         # Template loader + parameter substitution + execution
│   ├── templates_loader.py
│   └── templates/        # 5 .rq files
│       ├── impact_analysis.rq
│       ├── unused_modules.rq
│       ├── circular_deps.rq
│       ├── cascade_violations.rq
│       └── pattern_discovery.rq
├── cli/                  # Click CLI (codedna-export)
│   └── main.py           # export, validate, query commands
└── namespaces.py         # Central RDF namespace definitions
```

## OWL Ontology

The ArchGraph ontology (`synrax/schema/schema.owl`) defines:

| Class | Description |
|---|---|
| `arch:Module` | Source file with CodeDNA annotations |
| `arch:Package` | Directory / logical partition |
| `arch:Function` | Callable unit within a module |
| `arch:Export` | Public API symbol |
| `arch:Rule` | Architectural constraint from `rules:` field |
| `arch:AgentSession` | AI agent work session (append-only log) |
| `arch:Agent` | AI model instance |

Key properties:

- `arch:dependsOn` — **transitive** (`owl:TransitiveProperty`): full chain discovery
- `arch:usedBy` — **inverse** of `dependsOn` (`owl:inverseOf`): auto-generated reverse perspective
- `arch:cascades` — **subproperty** of `usedBy` (`rdfs:subPropertyOf`): enforces `[cascade]` semantics

## SHACL Shapes

6 validation shapes in `synrax/schema/shapes.ttl`:

| Shape | Target | Severity | Checks |
|---|---|---|---|
| `RulePresenceShape` | Module | Warning | Has ≥1 `hasRule` |
| `ModuleCompletenessShape` | Module | Violation | Has `moduleName` + `purpose` |
| `ExportCompletenessShape` | Export | Violation | Has `exportName` |
| `AgentSessionShape` | AgentSession | Violation/Warning | Has `sessionDate` + `belongs` + `narrative` |
| `CascadeCompletenessShape` | Module | Warning | ≤10 cascade targets |
| `PackageCompletenessShape` | Package | Violation | Has `packageName` + `purpose` |

## SPARQL Query Templates

| Template | Parameters | Purpose |
|---|---|---|
| `impact_analysis` | `module` | All modules transitively affected by changes to `module` |
| `unused_modules` | — | Orphan modules nothing depends on |
| `circular_deps` | — | Circular dependency detection via property paths |
| `cascade_violations` | — | Agent sessions that edited a module but skipped its `[cascade]` targets |
| `pattern_discovery` | — | Cross-cutting defects (e.g., soft-delete without `deleted_at` filter) |

## Testing

```bash
pytest                    # 91 tests, ~4s
pytest -x --tb=short      # fail-fast
python benchmarks.py      # reproduce all benchmark numbers
```

91 tests across 13 files:

| File | Tests | Scope |
|---|--:|---|
| `test_cli.py` | 10 | CLI commands, exit codes, file I/O |
| `test_codedna_vs_synrax.py` | 10 | Quantitative CodeDNA-vs-Synrax comparison |
| `test_engine.py` | 5 | SPARQL execution, parameter substitution |
| `test_manifest.py` | 5 | `.codedna` YAML parsing |
| `test_module_parser.py` | 8 | Docstring extraction (Level 1 + 2) |
| `test_pipeline.py` | 1 | Basic integration |
| `test_pipeline_advanced.py` | 7 | Edge cases: no manifest, syntax errors, skip rules |
| `test_query.py` | 3 | Template loading |
| `test_reasoner_advanced.py` | 6 | OWL-RL: transitivity, inverse, cascade→usedBy |
| `test_schema.py` | 5 | Schema/shape loading, basic reasoning |
| `test_sparql_templates.py` | 10 | All 5 SPARQL templates functional tests |
| `test_validator.py` | 10 | SHACL: conforms/violations/warnings/statistics |
| `test_value_add.py` | 11 | E2E pipeline + paper-driven value-add |

## Tech Stack

| Component | Library | Role |
|---|---|---|
| RDF serialization | rdflib ≥7.0 | Graph creation, Turtle I/O, SPARQL |
| OWL reasoning | owlrl ≥6.0 | OWL-RL entailment (pure Python) |
| SHACL validation | pyshacl ≥0.25 | Shape validation + reports |
| CLI | Click ≥8.1 | `codedna-export` entry point |
| Testing | pytest ≥8.0 | 91 tests |

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
