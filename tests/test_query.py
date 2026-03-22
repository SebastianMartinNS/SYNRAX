"""tests/test_query.py — Tests for SPARQL query templates."""

from synrax.query.templates_loader import list_templates, load_template


def test_list_templates():
    templates = list_templates()
    assert "impact_analysis" in templates
    assert "cascade_violations" in templates
    assert "circular_deps" in templates
    assert "unused_modules" in templates
    assert "pattern_discovery" in templates


def test_load_template_impact_analysis():
    query = load_template("impact_analysis")
    assert "SELECT" in query
    assert "arch:dependsOn" in query


def test_load_template_not_found():
    import pytest
    with pytest.raises(FileNotFoundError, match="not_a_real_template"):
        load_template("not_a_real_template")
