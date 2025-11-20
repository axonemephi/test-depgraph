import textwrap
from pathlib import Path

from depgraph.parsing.ast_parser import ASTParser


def test_ast_parser_extracts_all_import_shapes(tmp_path: Path):
    code = textwrap.dedent(
        """
        import os
        import sys as system
        from json import dumps
        from os.path import join as j
        from . import localmod
        from .pkg import submod
        """
    )
    file_path = tmp_path / "module.py"
    file_path.write_text(code, encoding="utf-8")

    imports = ASTParser.get_imports_from_file(file_path)

    assert "os" in imports
    assert "sys" in imports  # alias should resolve to original module name
    assert "json.dumps" in imports
    assert "os.path.join" in imports
    assert "." in imports  # from . import localmod
    assert ".pkg" in imports  # from .pkg import submod

