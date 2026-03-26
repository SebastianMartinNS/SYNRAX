# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML manifests + Python docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL-RL reasoning,
and exposes SPARQL queries for architectural impact analysis.

It also provides an **incremental runtime** with a JSON-RPC server (`codedna-export serve`)
that lets AI agents query the knowledge graph live during coding sessions.
The runtime acts as a **negative filter**: instead of answering questions directly, it shows
agents what they *don't* know yet — unexplored dependencies, missing coverage, out-of-scope files —
inducing more targeted exploration and reducing noise in the context window.

## Problem

CodeDNA gives you structured annotations in source code. But annotations alone can't answer:

- *"If I modify `db/connection.py`, what breaks?"* — requires transitive dependency tracking
- *"Are there orphan modules nobody depends on?"* — requires global graph analysis
- *"Did the AI agent miss a `[cascade]` target?"* — requires formal enforcement
- *"What does this module actually import?"* — requires AST-level analysis, not just annotations
- *"How much of the impact zone have I explored?"* — requires boundary tracking
- *"Which files are irrelevant to this task?"* — requires scope filtering

Synrax turns flat annotations into a **queryable knowledge graph** that answers all of
these with a single SPARQL query each. Ground-truth `import` analysis supplements
annotation-declared dependencies, so the graph stays accurate even when annotations lag behind code.

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
| SPARQL query templates | 0 | 9 | from zero |
| Node reach (5-node chain) | 1 hop | 4 hops | 4× depth |

**End-to-end pipeline** (6 modules): **< 500 ms**.
Full report: [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md)

## Architecture

```
Source (.codedna manifest + Python docstrings)
  → Extract (Python AST + YAML parser → RDF/Turtle)
    → Import Analysis (AST-based ground-truth dependency edges)
      → Reason (OWL-RL: transitive closure, inverse properties, subproperty propagation)
        → Validate (SHACL shapes → violation/warning report)
          → Query (9 SPARQL templates → JSON results)
            → Runtime (SessionGraph + JSON-RPC server for live agent queries)
              → Boundary Analysis (exploration tracking, node roles, scope filtering)
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

# Extract with project-specific schema extensions
codedna-export export demo/codebase -o graph.ttl --schema hw.owl --shapes hw_shapes.ttl

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

# Start the runtime JSON-RPC server for live agent queries
codedna-export serve demo/codebase --pre-ingest
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
│   ├── import_analyzer.py # AST-based import analysis → ground-truth dependency edges
│   └── pipeline.py       # Codebase walker + graph merger
├── schema/               # OWL ontology + SHACL validation
│   ├── schema.owl        # ArchGraph OWL ontology (10 classes, transitive/inverse properties)
│   ├── shapes.ttl        # 6 SHACL shapes (completeness, consistency, warnings)
│   ├── reasoner.py       # OWL-RL entailment via owlrl
│   ├── validator.py      # SHACL validation via pyshacl → JSON report
│   └── loader.py         # Schema/shape file loader (+ dynamic extension discovery)
├── query/                # SPARQL query engine
│   ├── engine.py         # Template loader + parameter substitution + execution
│   ├── templates_loader.py
│   └── templates/        # 9 .rq files
│       ├── impact_analysis.rq    # Transitive impact of module changes
│       ├── deps_of.rq            # Dependencies of a module
│       ├── rules_zone.rq         # Rules for a module and its impact zone
│       ├── unused_modules.rq     # Orphan modules
│       ├── circular_deps.rq      # Circular dependency detection
│       ├── cascade_violations.rq # Missed [cascade] targets
│       ├── pattern_discovery.rq  # Cross-cutting defect patterns
│       ├── node_roles.rq         # Hub/leaf/connector classification
│       └── out_of_scope.rq       # Files outside the current impact zone
├── runtime/              # Incremental runtime for live agent sessions
│   ├── session_graph.py  # SessionGraph: incremental graph + lazy OWL-RL + boundary tracking
│   └── tools.py          # 6 agent-callable tool functions
├── cli/                  # Click CLI (codedna-export)
│   └── main.py           # export, validate, query, serve commands
└── namespaces.py         # Central RDF namespace definitions
```

## OWL Ontology

The ArchGraph ontology (`synrax/schema/schema.owl`) defines 10 classes:

| Class | Description |
|---|---|
| `arch:Module` | Source file with CodeDNA annotations |
| `arch:Package` | Directory / logical partition |
| `arch:Function` | Callable unit within a module |
| `arch:Export` | Public API symbol |
| `arch:Rule` | Architectural constraint from `rules:` field |
| `arch:Constraint` | Formal constraint on a module or package |
| `arch:DependencyChain` | Materialized transitive dependency path |
| `arch:AgentSession` | AI agent work session (append-only log) |
| `arch:Agent` | AI model instance |
| `arch:Violation` | SHACL violation record linked to a session |

Key properties:

- `arch:dependsOn` — **transitive** (`owl:TransitiveProperty`): full chain discovery
- `arch:usedBy` — **inverse** of `dependsOn` (`owl:inverseOf`): auto-generated reverse perspective
- `arch:cascades` — **subproperty** of `usedBy` (`rdfs:subPropertyOf`): enforces `[cascade]` semantics
- `arch:packageDependsOn` — **transitive** package-level dependency (domain: `Package`)
- `arch:packageUsedBy` — **inverse** of `packageDependsOn`: auto-generated reverse

The base schema is generic. Project-specific classes (e.g., `HardwareModule`, `PhysicalConstraint`)
are loaded via the **extensions** mechanism — see [Schema Extensions](#schema-extensions) below.

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

9 templates in `synrax/query/templates/`:

| Template | Parameters | Purpose |
|---|---|---|
| `impact_analysis` | `module` | All modules transitively affected by changes to `module` |
| `deps_of` | `module` | All modules that `module` depends on |
| `rules_zone` | `module` | Architectural rules for a module and its transitive impact zone |
| `unused_modules` | — | Orphan modules nothing depends on |
| `circular_deps` | — | Circular dependency detection (on reasoned graph) |
| `cascade_violations` | — | Agent sessions that edited a module but skipped `[cascade]` targets |
| `pattern_discovery` | — | Cross-cutting defects (e.g., soft-delete without `deleted_at` filter) |
| `node_roles` | — | Classify modules as hub, leaf, or connector by degree |
| `out_of_scope` | `module` | Files outside the transitive impact zone of `module` |

## Testing

```bash
pytest                    # 185 tests, ~11s
pytest -x --tb=short      # fail-fast
python benchmarks.py      # reproduce all benchmark numbers
```

185 tests across 17 files:

| File | Tests | Scope |
|---|--:|---|
| `test_cli.py` | 10 | CLI commands, exit codes, file I/O |
| `test_cli_serve.py` | 8 | JSON-RPC serve command, ingest, query methods |
| `test_codedna_vs_synrax.py` | 10 | Quantitative CodeDNA-vs-Synrax comparison |
| `test_engine.py` | 5 | SPARQL execution, parameter substitution |
| `test_import_analyzer.py` | 17 | AST import resolution, graph building, edge cases |
| `test_manifest.py` | 5 | `.codedna` YAML parsing |
| `test_module_parser.py` | 8 | Docstring extraction (Level 1 + 2) |
| `test_pipeline.py` | 1 | Basic integration |
| `test_pipeline_advanced.py` | 7 | Edge cases: no manifest, syntax errors, skip rules |
| `test_query.py` | 3 | Template loading |
| `test_reasoner_advanced.py` | 6 | OWL-RL: transitivity, inverse, cascade→usedBy |
| `test_runtime_tools.py` | 18 | Agent tool functions: impact, deps, rules, status, boundary, tension |
| `test_schema.py` | 5 | Schema/shape loading, basic reasoning |
| `test_session_graph.py` | 50 | Incremental ingestion, lazy reasoning, boundary tracking, node roles, tension, provenance |
| `test_sparql_templates.py` | 10 | All 9 SPARQL templates functional tests |
| `test_validator.py` | 11 | SHACL: conforms/violations/warnings/statistics, package regression |
| `test_value_add.py` | 11 | E2E pipeline + paper-driven value-add |

## Tech Stack

| Component | Library | Role |
|---|---|---|
| RDF serialization | rdflib ≥7.0 | Graph creation, Turtle I/O, SPARQL |
| OWL reasoning | owlrl ≥6.0 | OWL-RL entailment (pure Python) |
| SHACL validation | pyshacl ≥0.25 | Shape validation + reports |
| CLI | Click ≥8.1 | `codedna-export` entry point |
| Testing | pytest ≥8.0 | 185 tests |
| YAML parsing | PyYAML ≥6.0 | .codedna manifest + extension discovery |

## Schema Extensions

The base ontology (`schema.owl`) and shapes (`shapes.ttl`) are generic.
Project-specific classes and constraints are loaded dynamically via:

1. **`.codedna` manifest** — `extensions` field auto-discovers extra files:
   ```yaml
   project: my-iot-device
   extensions:
     schema: [schema_hw.owl, schema_radio.owl]
     shapes: [shapes_hw.ttl]
   ```
2. **CLI flags** — `--schema` and `--shapes` on `export` / `validate` commands.

Both sources are merged at load time. This keeps the core schema clean while
allowing any project to define domain-specific OWL classes and SHACL shapes.

## Runtime (Agent Integration)

Synrax provides an **incremental runtime** for live AI coding sessions:

```bash
# Start the JSON-RPC server (stdin/stdout)
codedna-export serve path/to/codebase --pre-ingest
```

**JSON-RPC methods:**

| Method | Params | Description |
|---|---|---|
| `synrax.ingest` | `path` | Parse a file's annotations + imports, add to graph |
| `synrax.query_impact` | `module` | Transitively affected files if module changes |
| `synrax.query_deps` | `module` | All dependencies of a module |
| `synrax.query_rules` | `module` | Architectural rules for module and its impact zone |
| `synrax.status` | — | Graph statistics: triples, files, orphans, cycles |

The runtime uses **lazy reasoning** — OWL-RL is only re-applied when the graph
has changed and a query is executed. This keeps ingestion fast (< 10ms per file)
while queries always see the fully-reasoned graph.

### Agent Tool Functions

`make_synrax_tools(session)` returns 6 callable functions for agent integration:

| Tool | Purpose |
|---|---|
| `query_impact(module)` | Files transitively affected by changes (direct vs transitive, with provenance) |
| `query_deps(module)` | All dependencies of a module |
| `query_rules(module)` | Architectural rules for module and its impact zone |
| `query_graph_status()` | Triple count, orphan modules, circular dependencies |
| `query_boundary()` | Exploration progress: % explored, remaining in-scope, out-of-scope |
| `query_tension()` | Tension level: how much of the blast zone remains unexplored |

All tools return plain strings and never raise exceptions to callers.

### Boundary Tracking

The `SessionGraph` tracks which files the agent has visited and computes an exploration boundary:

- **`explored_pct`**: percentage of the impact zone that has been read
- **`remaining_in_scope`**: files in the impact zone not yet visited
- **`out_of_scope`**: files irrelevant to the current task (via `out_of_scope.rq`)
- **Node roles**: hub (high connectivity), leaf (no dependents), connector (bridges zones)
- **Tension engine**: quantifies unexplored blast zone (ratio, high-impact unvisited files)
- **Edge provenance**: each dependency edge tracked as `structural`, `annotated`, or `inferred`

This acts as a **negative filter** — showing the agent what it *hasn't* explored yet,
inducing more targeted navigation instead of random file reading.

### Programmatic Usage

```python
from synrax.runtime.session_graph import SessionGraph
from synrax.runtime.tools import make_synrax_tools

session = SessionGraph(Path("my_project"))
session.ingest_file("db/connection.py")
session.ingest_file("models/order.py")

tools = make_synrax_tools(session)
print(tools["query_impact"]("db/connection.py"))
print(tools["query_graph_status"]())
print(tools["query_boundary"]())
```

## Agent Benchmark (SWE-bench Style)

`benchmark_agent.py` runs a controlled experiment: an LLM agent navigates real open-source
codebases (click, rich, httpx) via tool calls, answering dependency analysis questions.
Each question is run twice — **raw** (filesystem tools only) vs **synrax** (filesystem + knowledge graph).

```bash
# Dry run — show tasks + ground truth, no API calls
py benchmark_agent.py --dry-run

# Single repo, default model
OPENROUTER_API_KEY=... py benchmark_agent.py --repo click

# Full matrix — all repos × all models
OPENROUTER_API_KEY=... py benchmark_agent.py --all-repos --all-models
```

### Double Helix Integration

In synrax mode, the benchmark implements the **Double Helix** pattern from the reference
SWE-bench runner — CodeDNA Layer 1 annotations and Synrax Layer 2 graph analysis
interleave seamlessly:

- **`[Synrax Navigation]` blocks** injected at the top of every `read_file()` result:
  Used-by (capped 3), Depends-on (capped 5), Rules, and Boundary status — each edge
  labeled with provenance (`annotated` / `structural` / `inferred`)
- **`[Synrax Tension Alert]`** injected mid-conversation every 3 file reads when
  blast-zone coverage is < 80%, naming high-impact unvisited files
- **Quick Map** in the system prompt showing the most-connected modules
- **Read cache** deduplicates repeated file reads (returns 300-char snippet)
- **All 6 Synrax tools** exposed: `query_impact`, `query_deps`, `query_rules`,
  `query_graph_status`, `query_boundary`, `query_tension`
- **`mark_visited()`** called on every file read — boundary and tension update live

### Metrics

| Metric | Description |
|---|---|
| F1 | Harmonic mean of precision and recall |
| Precision | Correct modules / predicted modules |
| Recall | Correct modules / ground-truth modules |
| Pass@1 | 1 if F1 ≥ 0.5, else 0 |
| Tool calls | Total tool invocations per question |
| Files read | Unique files read by the agent |
| Tokens | Total prompt + completion tokens consumed |

Ground truth is computed from AST dependency graphs — not hand-written keywords.

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
