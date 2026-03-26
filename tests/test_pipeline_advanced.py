"""tests/test_pipeline_advanced.py — Extended pipeline tests and edge cases."""

from pathlib import Path

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF


def test_pipeline_no_manifest(tmp_path: Path):
    """Pipeline should work even without a .codedna manifest."""
    # Create a Python file with CodeDNA docstring but no manifest
    py_file = tmp_path / "service.py"
    py_file.write_text(
        '''\
"""service.py — User authentication service.

exports: login(email, password) -> bool
used_by: api/routes.py -> handle_login
rules:   Must hash passwords with bcrypt. Never store plaintext.
agent:   test-model | test-provider | 2026-01-01 | Initial.
"""


def login(email: str, password: str) -> bool:
    """Authenticate a user.

    Rules: Must validate email format before DB lookup.
    """
    return True
''',
        encoding="utf-8",
    )

    g = extract_codebase(tmp_path)
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 1
    # No packages since no manifest
    packages = list(g.subjects(RDF.type, ARCH.Package))
    assert len(packages) == 0


def test_pipeline_no_python_files(tmp_path: Path):
    """Pipeline should still return a graph with manifest data if no .py files exist."""
    manifest = tmp_path / ".codedna"
    manifest.write_text("project: empty-project\npackages:\n  api/:\n    purpose: Empty\n")

    g = extract_codebase(tmp_path)
    packages = list(g.subjects(RDF.type, ARCH.Package))
    assert len(packages) == 1
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 0


def test_pipeline_skips_pycache(tmp_path: Path):
    """Pipeline should skip __pycache__ directories."""
    cache_dir = tmp_path / "__pycache__"
    cache_dir.mkdir()
    cache_file = cache_dir / "cached.py"
    cache_file.write_text('"""cached.py — Should be skipped.\n\nexports: none\nrules: test\n"""')

    g = extract_codebase(tmp_path)
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 0


def test_pipeline_skips_hidden_dirs(tmp_path: Path):
    """Pipeline should skip .hidden directories."""
    hidden = tmp_path / ".hidden"
    hidden.mkdir()
    py_file = hidden / "secret.py"
    py_file.write_text('"""secret.py — Hidden.\n\nexports: none\nrules: test\n"""')

    g = extract_codebase(tmp_path)
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 0


def test_pipeline_handles_syntax_errors(tmp_path: Path):
    """Pipeline should skip Python files with syntax errors gracefully."""
    bad = tmp_path / "broken.py"
    bad.write_text("def foo(\n  # missing closing paren")

    good = tmp_path / "good.py"
    good.write_text(
        '"""good.py — Works fine.\n\nexports: run() -> None\nrules: Test rule.\n"""',
        encoding="utf-8",
    )

    g = extract_codebase(tmp_path)
    # Should still get the good file
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 1


def test_pipeline_empty_directory(tmp_path: Path):
    """Pipeline on empty directory should return empty graph."""
    g = extract_codebase(tmp_path)
    assert len(g) == 0


def test_pipeline_multiple_modules(tmp_path: Path):
    """Pipeline should merge multiple module files."""
    for name in ["alpha", "beta", "gamma"]:
        f = tmp_path / f"{name}.py"
        f.write_text(
            f'"""{name}.py \u2014 Module {name}.\n\nexports: run() -> None\nrules: Test.\n"""',
            encoding="utf-8",
        )

    g = extract_codebase(tmp_path)
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) == 3
