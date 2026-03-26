"""Tests for synrax/extract/import_analyzer.py — AST-based import resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from synrax.extract.import_analyzer import (
    analyze_imports,
    build_import_graph,
    get_importers,
    resolve_import_to_file,
)
from synrax.namespaces import ARCH, RDF


@pytest.fixture()
def project_tree(tmp_path: Path) -> Path:
    """Create a project tree with real import statements."""
    enc = {"encoding": "utf-8"}

    # db/connection.py — leaf module, no intra-project imports
    (tmp_path / "db").mkdir()
    (tmp_path / "db" / "__init__.py").write_text("", **enc)
    (tmp_path / "db" / "connection.py").write_text(
        '"""db/connection.py - Database pool."""\n'
        "import os\n"
        "import json\n"
        "\ndef get_connection(): pass\n",
        **enc,
    )

    # models/__init__.py
    (tmp_path / "models").mkdir()
    (tmp_path / "models" / "__init__.py").write_text("", **enc)

    # models/order.py — imports db.connection
    (tmp_path / "models" / "order.py").write_text(
        '"""models/order.py - Order model."""\n'
        "from db.connection import get_connection\n"
        "\ndef create_order(data): pass\n",
        **enc,
    )

    # models/inventory.py — imports db.connection
    (tmp_path / "models" / "inventory.py").write_text(
        '"""models/inventory.py - Inventory model."""\n'
        "from db.connection import get_connection, execute_raw\n"
        "\ndef check_stock(): pass\n",
        **enc,
    )

    # forms/__init__.py
    (tmp_path / "forms").mkdir()
    (tmp_path / "forms" / "__init__.py").write_text("", **enc)

    # forms/order_form.py — imports models.order and models.inventory
    (tmp_path / "forms" / "order_form.py").write_text(
        '"""forms/order_form.py - Order validation."""\n'
        "from models.order import create_order\n"
        "from models.inventory import check_stock\n"
        "\ndef validate_order(): pass\n",
        **enc,
    )

    # views/checkout.py — imports forms.order_form
    (tmp_path / "views").mkdir()
    (tmp_path / "views" / "__init__.py").write_text("", **enc)
    (tmp_path / "views" / "checkout.py").write_text(
        '"""views/checkout.py - Checkout handler."""\n'
        "from forms.order_form import validate_order\n"
        "\ndef checkout_view(request): pass\n",
        **enc,
    )

    # notifications/email.py — imports models.order
    (tmp_path / "notifications").mkdir()
    (tmp_path / "notifications" / "__init__.py").write_text("", **enc)
    (tmp_path / "notifications" / "email.py").write_text(
        '"""notifications/email.py - Email sender."""\n'
        "from models.order import create_order\n"
        "\ndef send_confirmation(): pass\n",
        **enc,
    )

    return tmp_path


class TestResolveImport:
    def test_stdlib_excluded(self, tmp_path: Path):
        assert resolve_import_to_file("os", tmp_path) is None
        assert resolve_import_to_file("json", tmp_path) is None
        assert resolve_import_to_file("sys", tmp_path) is None

    def test_resolve_module_file(self, project_tree: Path):
        result = resolve_import_to_file("db.connection", project_tree)
        assert result is not None
        assert result.name == "connection.py"

    def test_resolve_package_init(self, project_tree: Path):
        result = resolve_import_to_file("db", project_tree)
        assert result is not None
        assert result.name == "__init__.py"

    def test_third_party_returns_none(self, project_tree: Path):
        assert resolve_import_to_file("django.db.models", project_tree) is None
        assert resolve_import_to_file("rdflib", project_tree) is None

    def test_nonexistent_returns_none(self, project_tree: Path):
        assert resolve_import_to_file("foo.bar.baz", project_tree) is None


class TestAnalyzeImports:
    def test_stdlib_imports_excluded(self, project_tree: Path):
        """db/connection.py only imports os and json — no intra-project deps."""
        results = analyze_imports(project_tree / "db" / "connection.py", project_tree)
        assert results == []

    def test_intra_project_imports(self, project_tree: Path):
        """models/order.py imports from db.connection."""
        results = analyze_imports(project_tree / "models" / "order.py", project_tree)
        assert len(results) == 1
        assert results[0]["module"] == "db/connection.py"
        assert results[0]["type"] == "from"

    def test_multiple_imports(self, project_tree: Path):
        """forms/order_form.py imports from models.order and models.inventory."""
        results = analyze_imports(project_tree / "forms" / "order_form.py", project_tree)
        modules = {r["module"] for r in results}
        assert modules == {"models/order.py", "models/inventory.py"}

    def test_deduplication(self, project_tree: Path):
        """Same module imported twice yields only one entry."""
        dup_file = project_tree / "dup_test.py"
        dup_file.write_text(
            "from db.connection import get_connection\nfrom db.connection import execute_raw\n",
            encoding="utf-8",
        )
        results = analyze_imports(dup_file, project_tree)
        assert len(results) == 1

    def test_syntax_error_returns_empty(self, project_tree: Path):
        bad_file = project_tree / "bad.py"
        bad_file.write_text("def broken(:\n  pass\n", encoding="utf-8")
        results = analyze_imports(bad_file, project_tree)
        assert results == []


class TestRelativeImports:
    def test_relative_import(self, tmp_path: Path):
        """from .sibling import X resolves within same package."""
        pkg = tmp_path / "pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        (pkg / "a.py").write_text("x = 1\n", encoding="utf-8")
        (pkg / "b.py").write_text("from .a import x\n", encoding="utf-8")

        results = analyze_imports(pkg / "b.py", tmp_path)
        assert len(results) == 1
        assert results[0]["module"] == "pkg/a.py"

    def test_parent_relative_import(self, tmp_path: Path):
        """from ..utils import X resolves to parent package."""
        pkg = tmp_path / "pkg" / "sub"
        pkg.mkdir(parents=True)
        (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
        (pkg / "__init__.py").write_text("", encoding="utf-8")
        (tmp_path / "pkg" / "utils.py").write_text("def helper(): pass\n", encoding="utf-8")
        (pkg / "mod.py").write_text("from ..utils import helper\n", encoding="utf-8")

        results = analyze_imports(pkg / "mod.py", tmp_path)
        assert len(results) == 1
        assert results[0]["module"] == "pkg/utils.py"


class TestBuildImportGraph:
    def test_full_graph(self, project_tree: Path):
        graph = build_import_graph(project_tree)
        # Check that dependsOn edges exist
        deps = set()
        for s, _p, o in graph.triples((None, ARCH.dependsOn, None)):
            # Get module names
            for _, _, sn in graph.triples((s, ARCH.moduleName, None)):
                str(sn)
            # o might not have moduleName if it's an import target not parsed
            deps.add((str(s), str(o)))

        # At minimum: models/order depends on db/connection
        order_uri = str(ARCH["models::order"])
        conn_uri = str(ARCH["db::connection"])
        assert (order_uri, conn_uri) in deps

    def test_graph_has_module_types(self, project_tree: Path):
        graph = build_import_graph(project_tree)
        modules = list(graph.triples((None, RDF.type, ARCH.Module)))
        assert len(modules) >= 4  # at least order, inventory, order_form, checkout


class TestGetImporters:
    def test_who_imports_connection(self, project_tree: Path):
        """db/connection.py is imported by models/order.py and models/inventory.py."""
        importers = get_importers("db/connection.py", project_tree)
        assert set(importers) == {"models/order.py", "models/inventory.py"}

    def test_who_imports_order(self, project_tree: Path):
        """models/order.py is imported by forms/order_form.py and notifications/email.py."""
        importers = get_importers("models/order.py", project_tree)
        assert set(importers) == {"forms/order_form.py", "notifications/email.py"}

    def test_leaf_has_no_importers(self, project_tree: Path):
        """views/checkout.py is not imported by anything."""
        importers = get_importers("views/checkout.py", project_tree)
        assert importers == []
