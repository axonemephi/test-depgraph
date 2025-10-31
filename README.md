# DepGraph

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**DepGraph** is a command-line tool to visualize Python project dependencies. It helps developers understand complex codebases by automatically generating visual maps of how modules are connected, making it easy to spot architectural problems like **circular dependencies** and untangle coupled code.

## 🎯 Features

- **Automatic Dependency Discovery**: Scans Python projects and builds a complete dependency graph
- **Cycle Detection**: Identifies circular dependencies that can lead to architectural issues
- **Flexible Visualization**: Multiple output formats including PNG, SVG, and HTML
- **Smart Filtering**: Exclude specific patterns, third-party libraries, or standard library modules
- **AST-Based Parsing**: Uses Python's Abstract Syntax Tree for accurate import detection

## 📋 Prerequisites

- Python 3.8 or higher
- [Graphviz](https://graphviz.org/download/) (for PNG/SVG output)

### Installing Graphviz

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows:**
Download and install from [Graphviz website](https://graphviz.org/download/)

## 🚀 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Kishan-Thanki/depgraph.git
cd depgraph
pip install -r requirements.txt
```

## 💡 Usage

### Basic Usage

Analyze a Python project and generate a dependency graph:

```bash
python src/depgraph/cli.py /path/to/your/project
```

This generates a `dependencies.png` file in your current directory.

### Using as a Module

You can also run DepGraph as a module:

```bash
python -m depgraph /path/to/your/project
```

### Advanced Options

Generate a different output format:

```bash
python src/depgraph/cli.py /path/to/project -o output.svg --format svg
```

Exclude specific directories or files:

```bash
python src/depgraph/cli.py /path/to/project -e venv -e tests -e "*.test.py"
```

Focus only on local code:

```bash
python src/depgraph/cli.py /path/to/project --no-third-party --no-stdlib
```

**Full help:**

```bash
python src/depgraph/cli.py --help
```

## 📁 Project Structure

```
depgraph/
├── src/
│   └── depgraph/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py                  # Command-line interface
│       ├── config.py               # Configuration management
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── dependency_graph.py # Core graph logic
│       │   └── module_node.py      # Module representation
│       ├── parsing/
│       │   ├── __init__.py
│       │   ├── ast_parser.py       # AST-based import parsing
│       │   └── project.py          # File discovery
│       └── rendering/
│           ├── __init__.py
│           ├── interface.py        # Visualization interface
│           └── visualizers.py      # Output implementations
├── requirements.txt
├── README.md
└── LICENSE
```

## 🏗️ Architecture

DepGraph follows a clean, modular architecture:

1. **CLI Layer** (`cli.py`): Handles user input and orchestrates the workflow
2. **Configuration** (`config.py`): Manages all settings and options
3. **Graph Layer** (`graph/`): Core data structures for the dependency graph
4. **Parsing Layer** (`parsing/`): Discovers files and extracts imports using AST
5. **Rendering Layer** (`rendering/`): Generates visualizations in various formats

## 🧩 Key Classes

- **`DepGraphCLI`**: Main entry point that handles command-line arguments
- **`DependencyGraph`**: Central data structure holding all module relationships
- **`ModuleNode`**: Represents a single Python module/file
- **`Project`**: Discovers and manages Python files in a project
- **`ASTParser`**: Extracts imports using Python's AST module
- **`GraphvizVisualizer`**: Renders graphs as PNG/SVG images
- **`HtmlVisualizer`**: Generates interactive HTML visualizations

## 🔍 How It Works

1. **Discovery**: Recursively scans the project directory for all `.py` files
2. **Parsing**: Uses Python's AST to extract import statements from each file
3. **Resolution**: Maps import strings to actual modules in the project
4. **Classification**: Categorizes modules as LOCAL, THIRD_PARTY, or STDLIB
5. **Analysis**: Detects circular dependencies using depth-first search
6. **Visualization**: Renders the graph using Graphviz or HTML

## 📝 Example Output

When you run DepGraph, you'll see output like:

```
Analyzing project: /path/to/my-project
Building dependency graph...
Found 42 modules
✓ No circular dependencies detected
Generating PNG visualization...
✓ Visualization saved to: dependencies.png
```

If circular dependencies are found:

```
⚠️  Warning: Found 2 circular dependency cycles!
  Cycle 1: app.models.user → app.services.auth → app.models.user
  Cycle 2: app.core.database → app.core.config → app.core.database
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built as part of a Software Design and Testing course project (IT643).
