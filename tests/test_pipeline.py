"""tests/test_pipeline.py — Integration test for the full extraction pipeline."""

from pathlib import Path

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF

FIXTURES = Path(__file__).parent / "fixtures"


def test_extract_codebase_merges_manifest_and_modules():
    g = extract_codebase(FIXTURES)
    # Should have packages from manifest
    packages = list(g.subjects(RDF.type, ARCH.Package))
    assert len(packages) >= 3

    # Should have modules from .py files
    modules = list(g.subjects(RDF.type, ARCH.Module))
    assert len(modules) >= 1

    # Total triples should be substantial
    assert len(g) > 20
