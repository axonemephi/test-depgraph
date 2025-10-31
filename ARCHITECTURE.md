# DepGraph Architecture Documentation

## Overview

DepGraph is a command-line tool for visualizing Python project dependencies. This document provides a detailed explanation of the architecture, classes, relationships, and design decisions.

## System Architecture

DepGraph follows a clean, modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer                             │
│                  (DepGraphCLI)                          │
│  - Argument parsing                                     │
│  - Workflow orchestration                               │
└──────────────────┬──────────────────────────────────────┘
                   │ uses
┌──────────────────┴──────────────────────────────────────┐
│              Configuration Layer                         │
│                   (Config)                               │
│  - Settings management                                  │
│  - Options storage                                      │
└──────────────────┬──────────────────────────────────────┘
                   │ uses
┌──────────────────┴──────────────────────────────────────┐
│              Parsing Layer                               │
│  ┌──────────────┐          ┌──────────────┐            │
│  │   Project    │          │  ASTParser   │            │
│  │ - Discovery  │          │  - Import    │            │
│  │ - Filtering  │          │    extraction│            │
│  └──────────────┘          └──────────────┘            │
└──────────────────┬──────────────────────────────────────┘
                   │ feeds into
┌──────────────────┴──────────────────────────────────────┐
│              Graph Layer                                 │
│  ┌────────────────────────────────────────┐            │
│  │      DependencyGraph                    │            │
│  │  - Node management                      │            │
│  │  - Dependency resolution                │            │
│  │  - Cycle detection                      │            │
│  └────────────────┬───────────────────────┘            │
│                   │ contains                            │
│  ┌────────────────┴───────────────────────┐            │
│  │         ModuleNode                      │            │
│  │  - Represents a Python module           │            │
│  │  - Tracks dependencies                  │            │
│  │  - Classified by ModuleType             │            │
│  └────────────────────────────────────────┘            │
└──────────────────┬──────────────────────────────────────┘
                   │ consumed by
┌──────────────────┴──────────────────────────────────────┐
│             Rendering Layer                              │
│  ┌─────────────────────────────────────────┐           │
│  │      IGraphVisualizer                    │           │
│  │           (interface)                    │           │
│  └────┬────────────────────────┬───────────┘           │
│       │ implements            │ implements             │
│  ┌────┴──────────┐  ┌─────────┴───────────┐           │
│  │ Graphviz      │  │   HtmlVisualizer    │           │
│  │ Visualizer    │  │                     │           │
│  │ - PNG/SVG     │  │ - Interactive       │           │
│  └───────────────┘  └─────────────────────┘           │
└────────────────────────────────────────────────────────┘
```

## Class Documentation

### 1. DepGraphCLI

**Purpose:** The Conductor - Main entry point that handles user interaction and orchestrates the entire workflow.

**Location:** `src/depgraph/cli.py`

**Responsibilities:**
- Parse command-line arguments using `argparse`
- Validate user input
- Create and configure the `Config` object
- Coordinate the pipeline: discovery → parsing → graph building → visualization
- Handle errors and provide user feedback

**Key Methods:**
- `main(args)`: Entry point that parses arguments and initiates execution
- `run(config)`: Orchestrates the complete analysis workflow
- `_create_parser()`: Configures the argument parser
- `_create_visualizer(format)`: Factory method for creating appropriate visualizers

**Relationships:**
- **Uses:** `Config`, `Project`, `ASTParser`, `DependencyGraph`, `IGraphVisualizer`
- **Creates:** Visualizer instances based on output format

**Design Pattern:** Facade - provides a simple interface to a complex subsystem

---

### 2. Config

**Purpose:** Holds all configuration settings for a DepGraph run.

**Location:** `src/depgraph/config.py`

**Responsibilities:**
- Store project path, output settings, and filtering options
- Provide a single source of truth for configuration
- Enable easy testing by allowing programmatic configuration

**Attributes:**
- `project_path` (Path): Root directory to analyze
- `output_file` (Path): Where to save the visualization
- `output_format` (str): 'png', 'svg', or 'html'
- `exclude_patterns` (List[str]): Glob patterns to exclude
- `show_third_party` (bool): Include third-party modules?
- `show_stdlib` (bool): Include standard library modules?

**Relationships:**
- **Used by:** `DepGraphCLI`, `DependencyGraph`, all visualizers

**Design Pattern:** Value Object - immutable data container

---

### 3. Project

**Purpose:** Represents the Python project being analyzed.

**Location:** `src/depgraph/parsing/project.py`

**Responsibilities:**
- Discover all Python files in the project directory
- Respect exclusion patterns
- Provide a clean interface for file discovery

**Key Methods:**
- `get_python_files(exclude_patterns)`: Recursively scan for .py files
- `_should_exclude(file_path, patterns)`: Check if a file matches exclusion patterns

**Relationships:**
- **Used by:** `DepGraphCLI`, `DependencyGraph`
- **Uses:** `Path` for file system operations

**Design Pattern:** Factory - creates lists of Path objects

---

### 4. ASTParser

**Purpose:** A stateless utility using Python's AST to extract imports from files.

**Location:** `src/depgraph/parsing/ast_parser.py`

**Responsibilities:**
- Parse Python files using the `ast` module
- Extract all import statements (import, from...import, etc.)
- Handle syntax errors gracefully
- Return raw import strings

**Key Methods:**
- `get_imports_from_file(file_path)`: Parse a file and return all imports as a Set[str]

**Internal Helper:**
- `_ImportVisitor`: AST NodeVisitor that walks the tree to collect imports

**Relationships:**
- **Used by:** `DepGraphCLI`, `DependencyGraph`
- **Uses:** Python's built-in `ast` module

**Design Pattern:** Utility/Tool - stateless, single-purpose class

**Design Benefits:**
- No execution required (safer than running imports)
- Handles complex cases like relative imports, aliases, etc.
- Graceful error handling for invalid syntax

---

### 5. ModuleNode

**Purpose:** The Brick - Represents a single Python module/file in the dependency graph.

**Location:** `src/depgraph/graph/module_node.py`

**Responsibilities:**
- Store module metadata (name, path, type)
- Track raw imports from the source file
- Maintain a set of resolved dependencies (other ModuleNodes)
- Support hashing for use in sets and dictionaries

**Attributes:**
- `name` (str): Fully qualified module name (e.g., 'app.models.user')
- `file_path` (Optional[Path]): Absolute path to the .py file
- `module_type` (ModuleType): Classification (LOCAL, THIRD_PARTY, STDLIB)
- `raw_imports` (Set[str]): Import strings from AST parsing
- `dependencies` (Set[ModuleNode]): Resolved dependencies (other nodes)

**Key Methods:**
- `__init__(name, file_path, module_type)`: Constructor
- `__repr__()`: Developer-friendly string representation
- `__eq__(other)`: Equality comparison based on module name
- `__hash__()`: Hash based on module name (enables set membership)

**Relationships:**
- **Used by:** `DependencyGraph`, `GraphVisualizer`
- **References:** Other `ModuleNode` instances (many-to-many dependency relationship)
- **Classified by:** `ModuleType` enum (1-to-1 relationship)

**Design Pattern:** Value Object - represents a conceptual entity

---

### 6. ModuleType (Enum)

**Purpose:** The Category - Classifies modules by their origin.

**Location:** `src/depgraph/graph/module_node.py`

**Values:**
- `LOCAL`: Modules within the analyzed project
- `THIRD_PARTY`: Externally installed packages
- `STDLIB`: Python standard library modules

**Purpose:**
- Enable visualization with different colors/styles
- Allow filtering of dependency types
- Provide insights into project architecture

**Relationships:**
- **Classifies:** Every `ModuleNode` has exactly one `ModuleType`

---

### 7. DependencyGraph

**Purpose:** The Blueprint - Central data structure holding the complete dependency graph.

**Location:** `src/depgraph/graph/dependency_graph.py`

**Responsibilities:**
- Store all ModuleNodes in a dictionary keyed by module name
- Build the graph from project files
- Resolve import strings to actual dependencies
- Classify modules by type
- Detect circular dependencies
- Apply filtering based on configuration

**Key Methods:**
- `build(project, parser, config)`: Main orchestration - builds the complete graph
- `add_node(node)`: Add a node to the graph
- `find_cycles()`: Detect circular dependencies using DFS
- `_create_module_node(file_path, project_root)`: Convert file path to ModuleNode
- `_resolve_dependencies()`: Map raw imports to actual ModuleNodes
- `_resolve_import(import_str, current_module)`: Resolve a single import
- `_resolve_relative_import(relative_str, current_module)`: Convert relative to absolute imports
- `_classify_modules()`: Determine if modules are local/third-party/stdlib
- `_apply_filters(config)`: Remove modules based on configuration

**Attributes:**
- `nodes` (Dict[str, ModuleNode]): Map of module names to nodes
- `_project_root` (Optional[Path]): Root directory of the project

**Relationships:**
- **Composed of:** Many `ModuleNode` instances (1-to-many aggregation)
- **Uses:** `Project` for file discovery, `ASTParser` for parsing, `Config` for settings
- **Consumed by:** `GraphVisualizer` for rendering

**Design Pattern:** Aggregate Root - manages a collection of entities

**Algorithm Details:**

**Cycle Detection:** Uses Depth-First Search (DFS) with recursion stack tracking:
- Maintain `visited` set for all processed nodes
- Maintain `rec_stack` for nodes in current path
- When a back edge is found (node points to node in recursion stack), a cycle exists
- Extract the cycle path and continue searching

**Import Resolution Strategy:**
1. Exact match: Check if import string exactly matches a module name
2. Prefix match: Check if any module starts with the import string
3. Relative imports: Resolve based on current module's location in hierarchy

---

### 8. IGraphVisualizer

**Purpose:** The Artist's Interface - Defines contract for visualization implementations.

**Location:** `src/depgraph/rendering/interface.py`

**Responsibilities:**
- Define the interface that all visualizers must implement
- Ensure consistent API across different output formats

**Key Methods:**
- `render(graph, config)`: Abstract method to generate visualization

**Relationships:**
- **Implemented by:** `GraphvizVisualizer`, `HtmlVisualizer`

**Design Pattern:** Strategy - allows interchangeable algorithms

---

### 9. GraphvizVisualizer

**Purpose:** Render dependency graphs as PNG or SVG images using Graphviz.

**Location:** `src/depgraph/rendering/visualizers.py`

**Responsibilities:**
- Create directed graphs using Graphviz DOT language
- Style nodes based on module type
- Layout edges between dependent modules
- Generate high-quality images

**Key Methods:**
- `render(graph, config)`: Generate PNG/SVG visualization
- `_add_node(dot, node)`: Add a node with appropriate styling
- `_escape_node_name(name)`: Make names Graphviz-safe
- `_add_title(dot, node_count)`: Add graph title

**Styling:**
- **LOCAL**: Blue nodes with light purple fill
- **THIRD_PARTY**: Orange nodes with dark red fill
- **STDLIB**: Gray nodes with light gray fill

**Relationships:**
- **Implements:** `IGraphVisualizer`
- **Uses:** Graphviz Python library (external dependency)
- **Renders:** `DependencyGraph` instances

---

### 10. HtmlVisualizer

**Purpose:** Generate interactive HTML visualizations (simplified implementation).

**Location:** `src/depgraph/rendering/visualizers.py`

**Responsibilities:**
- Create HTML output with embedded data
- Provide foundation for interactive visualization
- Display graph statistics

**Key Methods:**
- `render(graph, config)`: Generate HTML file
- `_generate_html(nodes, links)`: Create HTML structure

**Note:** Currently produces a simplified HTML page. Full implementation would use D3.js for interactive visualization.

**Relationships:**
- **Implements:** `IGraphVisualizer`
- **Uses:** Standard template approach

---

## Data Flow

### Complete Workflow

```
1. User invokes: python -m depgraph /path/to/project
                           ↓
2. DepGraphCLI.main() parses arguments
                           ↓
3. Config object created with user settings
                           ↓
4. Project discovers all .py files
                           ↓
5. ASTParser extracts imports from each file
                           ↓
6. DependencyGraph.build():
   - Creates ModuleNode for each file
   - Stores raw imports
   - Resolves dependencies
   - Classifies module types
   - Applies filters
                           ↓
7. DependencyGraph.find_cycles() detects circular dependencies
                           ↓
8. Appropriate Visualizer.render() generates output
                           ↓
9. Output saved to file, success message displayed
```

## Design Patterns Used

1. **Facade (DepGraphCLI)**: Simplifies complex subsystem interaction
2. **Factory (Project, Visualizers)**: Creates objects without specifying exact classes
3. **Strategy (IGraphVisualizer)**: Interchangeable visualization algorithms
4. **Value Object (Config, ModuleNode)**: Immutable data structures
5. **Aggregate Root (DependencyGraph)**: Manages entity collection
6. **Visitor (ASTParser._ImportVisitor)**: Operations on object structure

## Design Decisions

### Why AST Instead of Direct Execution?

- **Safety**: No code execution, avoiding side effects
- **Speed**: Parsing is faster than importing modules
- **Accuracy**: Works even with syntax errors or missing dependencies
- **Independence**: Doesn't require all dependencies to be installed

### Why Separate Parsing from Graph Building?

- **Single Responsibility**: Each class has one clear purpose
- **Testability**: Can test parsing independently
- **Reusability**: Parser could be used for other tools

### Why Multiple Visualizers?

- **Flexibility**: Different formats for different needs
- **Extensibility**: Easy to add new output formats
- **Separation**: Rendering logic isolated from analysis logic

### Why Dict of Nodes by Name?

- **O(1) Lookup**: Fast import resolution
- **Uniqueness**: Module names are unique identifiers
- **Simplicity**: Natural mapping of names to nodes

## Future Enhancements

1. **Interactive HTML**: Full D3.js implementation for zoomable, searchable graphs
2. **Edge Weighting**: Show dependency strength or frequency
3. **Clustering**: Automatically group related modules
4. **Export Formats**: JSON, YAML for programmatic access
5. **Real-time Mode**: Watch for file changes and auto-update
6. **Metrics**: Calculate coupling, cohesion scores
7. **Diff Mode**: Compare dependency graphs across versions

## Testing Strategy

### Unit Tests
- Test each class in isolation
- Mock dependencies for integration points
- Validate edge cases (empty projects, circular imports, etc.)

### Integration Tests
- Test complete pipeline with sample projects
- Verify output quality and correctness
- Test error handling and recovery

### Performance Tests
- Measure time complexity for large projects (1000+ files)
- Profile memory usage
- Optimize hot paths

## Security Considerations

- **Path Traversal**: All paths are validated and resolved
- **File Reading**: AST parsing avoids code execution
- **Output Validation**: Sanitize user inputs for file operations
- **Resource Limits**: Consider timeouts for very large projects

## Import Resolution Algorithm

### Overview

One of the most critical and complex aspects of DepGraph is correctly resolving import statements to actual modules in the graph. This involves handling multiple import patterns and edge cases.

### Import Extraction (AST Parser)

The `ASTParser` extracts import strings from Python files using Python's AST module:

**Absolute Imports:**
- `from os import path` → extracts `os.path`
- `import sys` → extracts `sys`
- `from config import Config` → extracts `config.Config`

**Relative Imports:**
- `from .TimeAccount import TimeAccount` → extracts `.TimeAccount`
- `from . import local` → extracts `.`
- `from ..parent import foo` → extracts `..parent.foo`

**Key Implementation Detail:** For relative imports, only the module path (not the imported class/function) is extracted. This allows the resolver to properly map relative imports to absolute paths before attempting to match imported items.

### Import Resolution (DependencyGraph)

The `DependencyGraph._resolve_import()` method handles three types of imports:

1. **Relative Imports**: Uses `_resolve_relative_import()` to convert relative paths to absolute module names
   - `.TimeAccount` from `accounts.InvestorAccount` → `accounts.TimeAccount`
   - `..parent.foo` from `a.b.c` → `parent.foo`

2. **Exact Matches**: Direct lookup in the nodes dictionary
   - `config` → `config` (if exists)

3. **Prefix Matching**: Uses `_get_import_variants()` to try parent modules
   - `config.Config` → tries `config.Config`, then `config`
   - `os.path.join` → tries `os.path.join`, then `os.path`, then `os`

### Algorithm Complexity

- **Time Complexity**: O(d * m) where d is the number of dependencies and m is the average module name depth
- **Space Complexity**: O(n) where n is the number of nodes
- **Optimization**: Uses dictionary lookups for O(1) exact matches

### Edge Cases Handled

1. **Circular Relative Imports**: Resolved to absolute paths before cycle detection
2. **Missing Modules**: Gracefully skipped, no errors thrown
3. **Third-Party vs Standard Library**: Correctly classified and optionally filtered
4. **Package vs Module Imports**: Handled through variant generation
5. **Deep Nesting**: Relative imports with multiple levels (e.g., `../../../parent`)

### Testing Import Resolution

The import resolution has been tested with:
- Real-world projects (Chronobank with 29 modules)
- Self-referential project (DepGraph analyzing itself)
- Various import patterns (absolute, relative, mixed)
- Standard library modules
- Third-party packages

