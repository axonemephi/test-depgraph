# DepGraph

> **Note:** This project is in the early stages of development and is not yet available for public installation. The instructions below are for running the tool from the source code.

A command-line tool to visualize project dependencies.

DepGraph helps you understand complex codebases by automatically generating a visual map of how your modules are connected. This makes it easy to spot architectural problems like **circular dependencies** and untangle coupled code.

Currently, DepGraph is in its initial phase with support for **Python** projects.

## Getting Started

Since the project is not yet published, you'll need to run it directly from the source code.

**Prerequisites:**

- Git
- Python 3.8+

**Setup:**

```bash
git clone https://github.com/Kishan-Thanki/depgraph.git
```

```bash
cd depgraph
```

```bash
pip install -r requirements.txt
```

## Usage

You must run the cli.py script directly using the Python interpreter from the root of the project directory.

**Basic Example:**

```bash
python src/depgraph/cli.py /path/to/your/project
```

This will generate a dependencies.png in your current folder.

For a full list of commands, run python src/depgraph/cli.py --help.
