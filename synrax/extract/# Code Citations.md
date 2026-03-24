# Code Citations

## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: BSD-3-Clause
https://github.com/rubinius/rubinius/blob/84368419a49767ef9549a5778812e5f54b6c6223/build/libraries/libffi/src/powerpc/ppc_closure.S

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/jamesgolick/enum_field/blob/bff7873bd0c48753a93f46e71f517da69fd5c7ce/MIT-LICENSE

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: unknown
https://github.com/nilsteampassnet/TeamPass/blob/ead1c7bd4f95191d58b842358fb804504f8557d9/licences/FOSSA-Licences-Report.md

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```


## License: MIT
https://github.com/mdvanes/grunt-kot2js/blob/769eb4271e7673f88ed6c352724723493d49b991/LICENSE-MIT

```
Now I have a full picture. The repo needs: **README.md**, **LICENSE**, **CONTRIBUTING.md**, and cleanup of `.gitignore` for `.ttl` test artifacts. Let me also check what test_output.ttl is (it's a generated artifact that should be ignored).I'm in **Ask mode** (read-only), so I can't create or edit files. But I can give you every file ready to paste/create. Here's the complete checklist and file contents for a GitHub-ready repo:

---

## Checklist: cosa manca per il push

| # | File | Stato | Azione |
|---|------|-------|--------|
| 1 | `README.md` | **Mancante** | Creare |
| 2 | `LICENSE` | **Mancante** | Creare (MIT, come da pyproject.toml) |
| 3 | `CONTRIBUTING.md` | **Mancante** | Creare |
| 4 | `.gitignore` | Presente ma incompleto | Aggiungere `test_output.ttl`, `demo/output.ttl` |
| 5 | `test_output.ttl` | **Artefatto generato** — non va nel repo | Eliminare e gitignore |
| 6 | `demo/output.ttl` | **Artefatto generato** | Già coperto da `*.ttl` nel gitignore |
| 7 | `synrax.egg-info/` | **Artefatto build** | Già in gitignore |
| 8 | `_reference/` | **Già escluso** | OK (in .gitignore) |
| 9 | `pyproject.toml` | Presente e completo | OK |
| 10 | `.github/copilot-instructions.md` | Presente | OK |
| 11 | `docs/BENCHMARK_REPORT.md` | Presente | OK |

---

## File 1: `README.md`

```markdown
# Synrax — ArchGraph

> Formal knowledge graph layer for [CodeDNA](https://github.com/Larens94/codedna)-annotated codebases.

Synrax extracts CodeDNA annotations (YAML + docstrings) into RDF triples,
validates them with SHACL shapes, infers transitive dependencies via OWL reasoning,
and exposes SPARQL queries for impact analysis.

## Why

CodeDNA gives you structured annotations in source code. Synrax turns them into a
**queryable knowledge graph** — so an AI agent (or a human) can ask:

- *"If I modify `db/connection.py`, what breaks?"* → 1 SPARQL query
- *"Are there orphan modules nobody uses?"* → 1 SPARQL query
- *"Did the agent miss a `[cascade]` target?"* → 1 SPARQL query

### Benchmark (6-module demo codebase)

| Metric | CodeDNA raw | Synrax | Delta |
|---|--:|--:|---|
| Knowledge triples | 296 | 1,315 | **+344%** |
| Dependency edges (transitive) | 10 | 26 | +16 |
| Inverse relations (`usedBy`) | 0 | 26 | from zero |
| Quality violations detected | 0 | 48 | from zero |
| SPARQL query templates | 0 | 5 | from zero |

Full pipeline runs in **< 500 ms**. See [docs/BENCHMARK_REPORT.md](docs/BENCHMARK_REPORT.md).

## Architecture

```
Source (.codedna + docstrings)
  → Extract (Python AST + YAML → RDF/Turtle)
    → Reason (OWL-RL: transitive closure, inverse properties)
      → Validate (SHACL shapes: completeness, consistency)
        → Query (SPARQL templates: impact, orphans, cycles, cascades)
```

## Install

```bash
pip install -e ".[dev]"
```

Requires **Python 3.11+**.

## Quick Start

```bash
# Extract + reason → Turtle file
codedna-export export demo/codebase -o graph.ttl

# Validate the graph
codedna-export validate graph.ttl

# Query: who is affected if I change db_connection?
codedna-export query impact_analysis graph.ttl -p module=db_connection

# Find orphan modules
codedna-export query unused_modules graph.ttl

# Detect circular dependencies
codedna-export query circular_deps graph.ttl
```

### CLI Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Validation failure (SHACL violations) |
| 2 | Parse error |

## Project Structure

```
synrax/
├── extract/          # CodeDNA parser (.codedna YAML + Python docstrings → RDF)
│   ├── manifest.py   # .codedna YAML parser
│   ├── module_parser.py  # Docstring AST parser (Level 1 + 2)
│   └── pipeline.py   # Full codebase extraction
├── schema/           # OWL ontology + SHACL shapes
│   ├── schema.owl    # ArchGraph OWL ontology
│   ├── shapes.ttl    # SHACL validation shapes
│   ├── reasoner.py   # OWL-RL reasoning (owlrl)
│   └── validator.py  # SHACL validation (pyshacl)
├── query/            # SPARQL query engine
│   ├── engine.py     # Template execution
│   └── templates/    # .rq files (impact, orphans, cycles, cascades, patterns)
├── cli/              # Click CLI (codedna-export)
└── namespaces.py     # RDF namespace definitions
```

## SPARQL Query Templates

| Template | Purpose |
|---|---|
| `impact_analysis` | Modules affected by changes to a given module |
| `unused_modules` | Orphan modules with no dependents |
| `circular_deps` | Circular dependency detection |
| `cascade_violations` | Agent sessions that missed `[cascade]` targets |
| `pattern_discovery` | Cross-cutting pattern defects (e.g., soft-delete without filter) |

## Tech Stack

- **RDF:** [rdflib](https://rdflib.readthedocs.io/) (serialization + SPARQL)
- **OWL Reasoning:** [owlrl](https://owl-rl.readthedocs.io/) (OWL-RL profile)
- **SHACL Validation:** [pyshacl](https://github.com/RDFLib/pySHACL)
- **CLI:** [Click](https://click.palletsprojects.com/)
- **Testing:** [pytest](https://pytest.org/) — 91 tests

## Testing

```bash
pytest                        # full suite (91 tests, ~4s)
pytest -x --tb=short          # quick fail-fast
py benchmarks.py              # reproduce all benchmark numbers
```

## Upstream

- [CodeDNA Protocol](https://github.com/Larens94/codedna) (v0.7)

## License

[MIT](LICENSE)
```

---

## File 2: `LICENSE`

```
MIT License

Copyright (c) 2026 Ab Es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## File 3: `CONTRIBUTING.md`

```
```

