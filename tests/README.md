# Tests Overview

This directory contains fast unit tests that exercise the critical pieces of DepGraph.

- `test_ast_parser.py` – verifies the AST parser understands absolute, relative, and aliased imports.
- `test_project.py` – ensures project discovery respects built-in/default exclusion patterns and that they can be disabled when needed.
- `test_dependency_graph.py` – covers dependency graph construction, relative import resolution, and circular dependency detection.

## Running the tests

```bash
pip install -r requirements.txt
pytest -q
```

All tests run without touching the sample projects under `examples/`.

