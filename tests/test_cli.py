"""Integration tests for the Tribeca Django Init CLI interfaces."""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402
from click.testing import CliRunner  # noqa: E402

from init_django.cli_mcp import main as mcp_main  # noqa: E402
from init_django.cli_user import main  # noqa: E402


@pytest.fixture
def temp_project_dir():
    """Create a temporary working directory for CLI tests."""
    d = tempfile.mkdtemp(prefix="tribeca_cli_test_")
    cwd = os.getcwd()
    os.chdir(d)
    yield Path(d)
    os.chdir(cwd)
    shutil.rmtree(d, ignore_errors=True)


def test_cli_basic_flow(temp_project_dir, monkeypatch):
    """Verify that the CLI runs with defaults and creates key files."""
    runner = CliRunner()
    # Simulate user choices for all steps (choose defaults)
    inputs = [
        "1",  # Reuse or create venv
        "1",  # Install dependencies
        "",  # Django version (default)
        "1",  # Initialize git
        "1",  # Create Django project
        "1",  # Create settings package
        # Only after settings prompt is complete, send app name:
        "users",  # App name
        "1",  # Create app
        "1",  # Apply migrations
        "1",  # Create .env file
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs) + "\n")
    assert result.exit_code == 0, f"Output:\n{result.output}"
    # Check if key files/folders were created
    assert (temp_project_dir / ".venv").exists() or (
        temp_project_dir / "manage.py"
    ).exists()
    assert (temp_project_dir / "README.md").exists()
    assert (temp_project_dir / "config" / "settings" / "base.py").exists()
    assert (temp_project_dir / "config" / "settings" / "dev.py").exists()
    assert (temp_project_dir / "config" / "settings" / "prod.py").exists()
    assert (temp_project_dir / ".env").exists()


def test_cli_skip_steps(temp_project_dir, monkeypatch):
    """Ensure skipping optional steps does not crash the CLI."""
    runner = CliRunner()
    # Simulate skipping venv and dependencies
    inputs = [
        "2",  # Skip venv
        "2",  # Skip dependencies
        "2",  # Skip git
        "2",  # Skip Django project
        "2",  # Skip settings
        # Only after settings prompt is complete, send app name:
        "users",  # App name
        "2",  # Skip app
        "2",  # Skip migrations
        "2",  # Skip .env file
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs) + "\n")
    assert result.exit_code == 0, f"Output:\n{result.output}"
    # README may not exist if all steps skipped
    # But project should not crash


def test_cli_custom_app_name(temp_project_dir, monkeypatch):
    """Check that providing a custom app name creates that app."""
    runner = CliRunner()
    app_name = "customapp"
    inputs = [
        "1",  # venv
        "1",  # deps
        "",  # Django version (default)
        "1",  # git
        "1",  # django project
        "1",  # settings
        # Only after settings prompt is complete, send app name:
        app_name,  # app name
        "1",  # create app
        "1",  # migrations
        "1",  # create .env file
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs) + "\n")
    assert result.exit_code == 0, f"Output:\n{result.output}"
    assert (temp_project_dir / app_name).exists() or (
        temp_project_dir / f"{app_name}"
    ).exists()
    assert (temp_project_dir / ".env").exists()


def test_cli_mcp_json_output(temp_project_dir):
    """Confirm MCP mode outputs JSON events including a final 'done'."""
    runner = CliRunner()
    result = runner.invoke(
        mcp_main,
        [
            "--json",
            "--venv",
            "skip",
            "--install-deps",
            "no",
            "--git-init",
            "no",
            "--project",
            "no",
            "--settings",
            "no",
            "--app-name",
            "users",
            "--app-create",
            "no",
            "--migrate",
            "no",
            "--readme",
            "no",
            "--env-file",
            "no",
        ],
    )
    assert result.exit_code == 0, f"Output:\n{result.output}"
    lines = result.output.splitlines()
    json_lines = [json.loads(line) for line in lines if line.startswith("{")]
    events = [j.get("event") for j in json_lines]
    assert "done" in events


def test_cli_requires_dependencies_user(temp_project_dir, monkeypatch):
    """Creating a project without installing dependencies should fail."""
    runner = CliRunner()
    inputs = [
        "1",  # create venv
        "2",  # skip dependencies
        "2",  # skip git
        "1",  # attempt project creation
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs) + "\n")
    assert result.exit_code != 0
    assert "django-admin not found" in result.output


def test_cli_requires_dependencies_mcp(temp_project_dir):
    """MCP mode should emit an error event when django-admin is missing."""
    runner = CliRunner()
    result = runner.invoke(
        mcp_main,
        [
            "--json",
            "--venv",
            "recreate",
            "--install-deps",
            "no",
            "--git-init",
            "no",
            "--project",
            "yes",
            "--settings",
            "no",
            "--app-name",
            "users",
            "--app-create",
            "no",
            "--migrate",
            "no",
            "--readme",
            "no",
            "--env-file",
            "no",
        ],
    )
    assert result.exit_code != 0
    lines = result.output.splitlines()
    json_lines = [json.loads(line) for line in lines if line.startswith("{")]
    project_errors = [
        j
        for j in json_lines
        if j.get("event") == "project" and j.get("status") == "error"
    ]
    assert project_errors
    assert "Install dependencies first" in project_errors[0]["message"]
