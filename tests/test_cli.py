import os
import shutil
import tempfile
from pathlib import Path
from click.testing import CliRunner
import pytest

from init_django.cli import main

@pytest.fixture
def temp_project_dir():
    d = tempfile.mkdtemp(prefix="tribeca_cli_test_")
    cwd = os.getcwd()
    os.chdir(d)
    yield Path(d)
    os.chdir(cwd)
    shutil.rmtree(d)


def test_cli_basic_flow(temp_project_dir, monkeypatch):
    runner = CliRunner()
    # Simulate user choices for all steps (choose defaults)
    inputs = [
        "1",  # Reuse or create venv
        "1",  # Install dependencies
        "1",  # Initialize git
        "1",  # Create Django project
        "1",  # Create settings package
        "users",  # App name
        "1",  # Create app
        "1"   # Apply migrations
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs))
    assert result.exit_code == 0
    # Check if key files/folders were created
    assert (temp_project_dir / ".venv").exists() or (temp_project_dir / "manage.py").exists()
    assert (temp_project_dir / "README.md").exists()
    assert (temp_project_dir / "config" / "settings" / "base.py").exists()
    assert (temp_project_dir / "config" / "settings" / "dev.py").exists()
    assert (temp_project_dir / "config" / "settings" / "prod.py").exists()


def test_cli_skip_steps(temp_project_dir, monkeypatch):
    runner = CliRunner()
    # Simulate skipping venv and dependencies
    inputs = [
        "2",  # Skip venv
        "2",  # Skip dependencies
        "2",  # Skip git
        "2",  # Skip Django project
        "2",  # Skip settings
        "users",  # App name
        "2",  # Skip app
        "2"   # Skip migrations
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs))
    assert result.exit_code == 0
    # README may not exist if all steps skipped
    # But project should not crash


def test_cli_custom_app_name(temp_project_dir, monkeypatch):
    runner = CliRunner()
    app_name = "customapp"
    inputs = [
        "1", "1", "1", "1", "1", app_name, "1", "1"
    ]
    monkeypatch.setenv("DJANGO_SECRET_KEY", "test-key")
    result = runner.invoke(main, input="\n".join(inputs))
    assert result.exit_code == 0
    assert (temp_project_dir / app_name).exists() or (temp_project_dir / f"{app_name}").exists()
