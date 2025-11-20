# Design Commentary

## Scope

DepCycle scans a Python project, builds a module-level dependency graph, highlights circular dependencies, and renders the graph as PNG/SVG (Graphviz) or HTML (placeholder).

## Key Design Decisions

### 1. Layered Architecture
- **CLI / Entry Points** (`depcycle.cli`) provide a façade that wires the workflow together.
- **Parsing Layer** (`parsing.project`, `parsing.ast_parser`) is responsible only for I/O and AST inspection. This keeps graph logic pure and easily testable.
- **Graph Layer** (`graph.dependency_graph`, `graph.module_node`) stores project state and resolves imports. It accepts parser/project abstractions so it can be reused or tested in isolation.
- **Rendering Layer** (`rendering.*`) implements a simple `IGraphVisualizer` strategy, enabling additional outputs without changing the analysis logic.

### 2. Default Exclusions as Guard Rails
Most real projects contain embedded virtual environments, caches, or `node_modules/`. DepCycle now ignores these by default within `Project.get_python_files()` but still lets callers opt out (`include_defaults=False`). This prevents massive, noisy graphs and significantly improves runtime without relying on the user to pass every exclusion.

### 3. Safe Import Extraction
All dependency discovery happens via Python's `ast` module rather than executing imports. This reduces risk, works even when dependencies are missing, and aligns with secure tooling guidelines.

## Principles Applied
- **Single Responsibility** – each module handles one concern (CLI orchestration, parsing, graph modeling, rendering).
- **Open/Closed Principle** – the `IGraphVisualizer` interface and `ModuleType` enum allow new renderers or classifications without modifying existing logic.
- **Dependency Inversion** – `DependencyGraph.build()` depends on the abstract `Project`+`ASTParser` API, so they can be mocked in tests.
- **Fail Fast** – CLI argument validation and project path checks stop execution before expensive work happens, improving UX.

## Refactor & Cleanup Notes
- Added default exclusion patterns (venv, node_modules, caches, etc.) to `Project.get_python_files()` and backed the logic with tests. Self-hosted repos often contain these folders; excluding them drops analysis time from minutes to seconds on the provided sample projects.
- Split dependencies into runtime (`graphviz`) and dev extras (`pytest`) via `pyproject.toml`. This keeps the installed wheel lean while allowing contributors to run `pip install -e .[dev]` to get the tooling they need.
- Introduced `tests/conftest.py` to prepend `src/` to `sys.path`, so the test suite executes against in-tree code without requiring an editable install. This simplifies CI and lowers the barrier for new contributors.

## Testing Strategy

Unit tests cover:
- AST parsing edge cases (absolute, relative, aliases).
- Project discovery with default and custom exclusions.
- Dependency graph build, relative import resolution, and cycle detection.

See `tests/README.md` for the exact list and execution instructions.