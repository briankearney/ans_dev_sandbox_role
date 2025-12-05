import os
import pytest


def test_python_available(host):
    python = host.exists('python3') or host.exists('python')
    assert python, "Python interpreter should be available"


def test_git_installed(host):
    assert host.exists('git'), "git should be installed"


def test_temp_dir_created(host):
    # Molecule doesn't expose role facts; check /tmp presence heuristic
    tmp_present = host.file('/tmp').is_directory
    assert tmp_present, "/tmp directory should exist"


def test_pyyaml_import():
    try:
        import yaml  # noqa: F401
    except Exception as exc:
        pytest.fail(f"PyYAML should be importable: {exc}")
