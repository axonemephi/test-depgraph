from pathlib import Path

from depgraph.parsing.project import Project


def test_project_discovers_python_files_with_default_excludes(tmp_path: Path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "a.py").write_text("import sys", encoding="utf-8")
    (tmp_path / "pkg" / "b.py").write_text("from . import a", encoding="utf-8")

    # directories that should be excluded automatically
    (tmp_path / "venv").mkdir()
    (tmp_path / "venv" / "fake.py").write_text("import nothing", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "noop.py").write_text("x = 1", encoding="utf-8")

    project = Project(tmp_path)
    files = project.get_python_files(exclude_patterns=["pkg/b.py"])

    names = {f.name for f in files}
    assert names == {"a.py"}


def test_project_can_opt_out_of_default_excludes(tmp_path: Path):
    (tmp_path / "venv").mkdir()
    (tmp_path / "venv" / "fake.py").write_text("x = 1", encoding="utf-8")

    project = Project(tmp_path)
    files = project.get_python_files(include_defaults=False)

    assert {f.name for f in files} == {"fake.py"}

