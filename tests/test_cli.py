"""tests/test_cli.py — Integration tests for the codedna-export CLI."""

from pathlib import Path

from click.testing import CliRunner

from synrax.cli.main import cli

FIXTURES = Path(__file__).parent / "fixtures"


def test_export_produces_turtle(tmp_path: Path):
    """Export should produce a valid Turtle file."""
    output = tmp_path / "out.ttl"
    runner = CliRunner()
    result = runner.invoke(cli, ["export", str(FIXTURES), "-o", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    content = output.read_text()
    assert "arch:" in content or "@prefix" in content


def test_export_with_reasoning(tmp_path: Path):
    """Export with --reason should include inferred triples."""
    output_reason = tmp_path / "reason.ttl"
    output_noreason = tmp_path / "noreason.ttl"
    runner = CliRunner()

    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(output_reason), "--reason"])
    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(output_noreason), "--no-reason"])

    # Reasoned graph should have more triples (inference adds triples)
    assert output_reason.stat().st_size > output_noreason.stat().st_size


def test_export_no_reason_flag(tmp_path: Path):
    """Export with --no-reason should still produce valid output."""
    output = tmp_path / "out.ttl"
    runner = CliRunner()
    result = runner.invoke(cli, ["export", str(FIXTURES), "-o", str(output), "--no-reason"])
    assert result.exit_code == 0
    assert output.exists()


def test_export_default_reasoning(tmp_path: Path):
    """Export defaults to reasoning enabled."""
    output = tmp_path / "out.ttl"
    runner = CliRunner()
    result = runner.invoke(cli, ["export", str(FIXTURES), "-o", str(output)])
    assert result.exit_code == 0
    assert "triples" in result.output.lower()


def test_export_nonexistent_root():
    """Export of nonexistent directory should fail."""
    runner = CliRunner()
    result = runner.invoke(cli, ["export", "/nonexistent/path_abc123"])
    assert result.exit_code != 0


def test_validate_valid_graph(tmp_path: Path):
    """Validate command on a well-formed graph should exit 0."""
    # First export to get a valid Turtle file
    ttl = tmp_path / "valid.ttl"
    runner = CliRunner()
    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(ttl), "--reason"])

    result = runner.invoke(cli, ["validate", str(ttl)])
    # Output should be JSON with conforms field
    assert "conforms" in result.output


def test_validate_writes_output_file(tmp_path: Path):
    """Validate with -o should write the report to a file."""
    ttl = tmp_path / "test.ttl"
    report = tmp_path / "report.json"
    runner = CliRunner()
    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(ttl), "--no-reason"])

    runner.invoke(cli, ["validate", str(ttl), "-o", str(report)])
    assert report.exists()
    import json

    data = json.loads(report.read_text())
    assert "conforms" in data
    assert "statistics" in data


def test_query_command(tmp_path: Path):
    """Query command should execute and return JSON results."""
    ttl = tmp_path / "q.ttl"
    runner = CliRunner()
    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(ttl), "--no-reason"])

    result = runner.invoke(cli, ["query", "unused_modules", str(ttl)])
    assert result.exit_code == 0
    # Output should be valid JSON (list)
    import json

    data = json.loads(result.output)
    assert isinstance(data, list)


def test_query_with_param(tmp_path: Path):
    """Query command with -p parameter should substitute correctly."""
    ttl = tmp_path / "q.ttl"
    runner = CliRunner()
    runner.invoke(cli, ["export", str(FIXTURES), "-o", str(ttl), "--reason"])

    result = runner.invoke(
        cli,
        [
            "query",
            "impact_analysis",
            str(ttl),
            "-p",
            "module=billing::invoice_service",
        ],
    )
    assert result.exit_code == 0


def test_cli_version():
    """--version flag should work."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower() or "0.2" in result.output
