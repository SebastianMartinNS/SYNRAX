# Contributing to Synrax

## Setup

```bash
git clone https://github.com/<your-user>/synrax.git
cd synrax
pip install -e ".[dev]"
pytest
```

## Code Style

- Python 3.11+, type hints on all public functions
- `pathlib.Path` for all file paths — never raw strings
- RDF namespaces from `synrax/namespaces.py` — never create ad-hoc `Namespace()`
- Docstrings follow CodeDNA Level 1/2 format (this project dogfoods the protocol)
- Lint with `ruff check .` (config in pyproject.toml)

## Testing

All changes must pass:

```bash
pytest -v               # 91 tests
ruff check .            # lint
```

New features need tests. Follow patterns in existing test files.

## Commit Messages

```
<component>: <short description>

Examples:
  extract: handle empty .codedna manifests
  schema: add SHACL shape for AgentSession
  query: fix parameter substitution in impact_analysis
  cli: add --format json flag to export
```

## Pull Requests

1. Fork and branch from `main`
2. Add tests for new functionality
3. Ensure `pytest` and `ruff check .` pass
4. Open a PR with a clear description
