"""tests/test_manifest.py — Tests for .codedna manifest parser."""

from pathlib import Path

import pytest
from rdflib import Literal
from rdflib.namespace import XSD

from synrax.extract.manifest import parse_manifest
from synrax.namespaces import ARCH, RDF

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_manifest_creates_packages():
    g = parse_manifest(FIXTURES / ".codedna")
    packages = list(g.subjects(RDF.type, ARCH.Package))
    assert len(packages) == 3


def test_parse_manifest_package_names():
    g = parse_manifest(FIXTURES / ".codedna")
    names = {str(o) for s, p, o in g.triples((None, ARCH.packageName, None))}
    assert "api/" in names
    assert "billing/" in names
    assert "reports/" in names


def test_parse_manifest_purposes():
    g = parse_manifest(FIXTURES / ".codedna")
    purposes = {str(o) for s, p, o in g.triples((None, ARCH.purpose, None))}
    assert "HTTP API endpoints" in purposes


def test_parse_manifest_depends_on():
    g = parse_manifest(FIXTURES / ".codedna")
    billing_uri = ARCH["test-project_billing"]
    api_uri = ARCH["test-project_api"]
    assert (billing_uri, ARCH.packageDependsOn, api_uri) in g


def test_parse_manifest_missing_project(tmp_path):
    bad = tmp_path / ".codedna"
    bad.write_text("packages:\n  api/:\n    purpose: test\n")
    with pytest.raises(ValueError, match="Missing required field 'project'"):
        parse_manifest(bad)
