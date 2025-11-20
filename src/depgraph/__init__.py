"""
DepGraph - A dependency graph visualization tool for Python projects.

DepGraph helps developers understand complex codebases by automatically 
generating visual maps of module dependencies.
"""

__version__ = "0.2.0"

from .cli import DepGraphCLI
from .config import Config
from .graph import DependencyGraph, ModuleNode, ModuleType
from .parsing import Project, ASTParser
from .rendering import IGraphVisualizer, GraphvizVisualizer, HtmlVisualizer

__all__ = [
    'DepGraphCLI',
    'Config',
    'DependencyGraph',
    'ModuleNode',
    'ModuleType',
    'Project',
    'ASTParser',
    'IGraphVisualizer',
    'GraphvizVisualizer',
    'HtmlVisualizer',
]

