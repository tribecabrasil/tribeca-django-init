import json
import subprocess

from init_django import cli_common


class DummyCompleted:
    def __init__(self, stdout="", stderr=""):
        self.stdout = stdout
        self.stderr = stderr


def test_run_success(monkeypatch, capsys):
    def dummy_run(*args, **kwargs):
        return DummyCompleted(stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", dummy_run)
    cli_common.run("echo ok")
    captured = capsys.readouterr()
    assert "ok" in captured.out


def test_emit_json_event(capsys):
    cli_common.emit_json_event("demo", "success", "msg", {"a": 1})
    out = capsys.readouterr().out.strip()
    data = json.loads(out)
    assert data["event"] == "demo"
    assert data["status"] == "success"
    assert data["data"]["a"] == 1


def test_create_helpers(tmp_path, monkeypatch):
    cmds = []

    def fake_run(cmd: str, check: bool = True):
        cmds.append(cmd)

    monkeypatch.setattr(cli_common, "run", fake_run)
    venv = tmp_path / ".venv"
    bin_dir = venv / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "django-admin").write_text("#!/bin/sh\n")
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "wsgi.py").write_text("app = None")

    cli_common.create_virtualenv(venv)
    cli_common.install_dependencies(venv, "5.2.3")
    cli_common.start_django_project(venv, tmp_path)
    cli_common.create_app(venv, "users")
    cli_common.apply_migrations(venv)
    cli_common.create_readme(tmp_path)
    cli_common.create_env_file(tmp_path)
    cli_common.create_settings_package(tmp_path)

    assert any("django-admin" in c for c in cmds)
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / ".env").exists()
    assert (tmp_path / "config" / "settings" / "base.py").exists()
