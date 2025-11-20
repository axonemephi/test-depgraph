from pathlib import Path

from depcycle.config import Config
from depcycle.graph.dependency_graph import DependencyGraph
from depcycle.parsing.ast_parser import ASTParser
from depcycle.parsing.project import Project


def write(tmp_dir: Path, rel: str, content: str):
    path = tmp_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_cycle_detection(tmp_path: Path):
    write(tmp_path, "pkg/a.py", "from . import b")
    write(tmp_path, "pkg/b.py", "from . import c")
    write(tmp_path, "pkg/c.py", "from . import a")

    project = Project(tmp_path)
    parser = ASTParser()
    graph = DependencyGraph()
    config = Config(project_path=tmp_path, output_file=tmp_path / "out.png")

    graph.build(project, parser, config)
    cycles = graph.find_cycles()

    assert len(graph) == 3
    assert any({node.name for node in cycle} == {"pkg.a", "pkg.b", "pkg.c"} for cycle in cycles)


def test_relative_import_resolution(tmp_path: Path):
    write(tmp_path, "x/y/z.py", "from ..u import v")
    write(tmp_path, "x/u/v.py", "pass")

    project = Project(tmp_path)
    parser = ASTParser()
    graph = DependencyGraph()
    config = Config(project_path=tmp_path, output_file=tmp_path / "out.png")

    graph.build(project, parser, config)

    node_map = {node.name: node for node in graph}
    assert "x.y.z" in node_map
    assert "x.u.v" in node_map
    assert "x.u.v" in {dep.name for dep in node_map["x.y.z"].dependencies}

