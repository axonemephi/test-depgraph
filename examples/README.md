Examples for trying DepGraph quickly

Contents
- basic_project: No cycles, simple layered imports
- cyclic_project: Intentional cycle between modules

How to run
- From repo root (this folder):

Basic (acyclic) graph, SVG:
```bash
depgraph "examples/basic_project" -o basic_deps.svg --format svg
```

Cyclic graph, SVG (shows cycle warning):
```bash
depgraph "examples/cyclic_project" -o cyclic_deps.svg --format svg
```

Tips
- Try adding or removing imports to see edges appear/disappear.
- Move an import to function scope to break a cycle without changing structure.
- Add -e "**/__pycache__" to ignore bytecode caches if present.



